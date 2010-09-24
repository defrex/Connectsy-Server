import uuid
from tornado.web import HTTPError
from pymongo import DESCENDING, GEO2D
#from bson import Code
#temp
class Code(object):
    def __init__(*args, **kwargs):
        pass

import db
from utils import timestamp, require_auth
from base_handlers import BaseHandler
from api.users.friends import status as friend_status
from api.friends.friend_utils import get_friends

class EventsHandler(BaseHandler):
    @require_auth
    def post(self):
        '''
        Creates a new event
        '''
        req_body = self.body_dict()
        response = {}
        event = {}

        #grab data from the user-supplied dict
        try:
            event[u'where'] = req_body[u'where']
            event[u'when'] = req_body[u'when']
            event[u'desc'] = req_body[u'desc']
            event[u'broadcast'] = req_body[u'broadcast']
            event[u'posted_from'] = req_body[u'posted_from']
            event[u'location'] = req_body.get(u'location', '')
            event[u'category'] = req_body.get(u'category', '') #optional field
        except KeyError, e:
            print e
            raise HTTPError(400) #TODO - detail what was missing
        else:
            event[u'creator'] = self.get_session()[u'username']
            event[u'created'] = int(timestamp())
            event[u'revision'] = uuid.uuid1().hex

            response[u'revision'] = event[u'revision']
            response[u'id'] = str(db.objects.event.insert(event))

        self.output(response, 201)

    @require_auth
    def get(self):
        '''
        Gets a list of events
        TODO - make the list relative to the user
        '''
        #store username for later use
        username = self.get_session()[u'username']

        #grab the sorting/filtering types from the args
        sort = self.get_argument('sort', None)
        filter = self.get_argument('filter', None)

        #prep filtering
        if filter == 'friends':
            #get the user's friends
            friends = get_friends(username)

            # Get a list of events started by friends
            # TODO

            # This is madness.
            # THIS IS CONNECTSY!
            # Here's how this mofo works:
            # First, we mapreduce the attendance collection to find
            # all unique events with with friends that are attending.
            #
            # We then take this resulting list of event_id's, and query
            # on them with a few parameters to determine whether they're
            # able to join the event, and also add a sort.  Rather than
            # sending the event data down the line, however, we just
            # transfer the revisions.

            #add the user to the friends list, for mapreduce reasons
            friends.append(username)

            # Limit MR'd entries to those from the friends + user
            query = {
                u'username': {u'$in': friends}
            }

            # Javascript map function - takes just the event_id and username
            # from the already-filtered collection
            map = Code("""function() {
                  emit(this.event, this.username, true);
            }""")

            # Javascript reduce function.  Returns [event_id, invited], where
            # invited is a boolean stating whether the user has been invited.
            reduce = Code("""function(key, values) {
                // if values.length == 1, the user is either not
                // invited, or is the only invitee; either way
                // we don't want to set "invited"
                if (values.length > 1)
                    for (var i=0; i<values.length; i++)
                        if (values[i] == "%s")
                            return [key, true];

                // if the user wasn't in the list of attendees for this
                // event, then he's not invited
                return [key, false];
            }""" % username) #TODO - sanitize me cap'n

            event_list = db.objects.attendance.mapreduce

        #any other value for filter is a category
        elif filter:
            filter = {u'category': filter}
        else:
            filter = {}

        #set up the base query
        if sort is None or sort == u'nearby':
            #make sure there's a default sort here
            sort = sort or 'soon'

            #grab lat/lng from the query, defaulting to toronto
            lat = float(self.get_argument('lat', '43.652527'))
            lng = float(self.get_argument('lng', '-79.381961'))
            where = [lat, lng]
            q = {u'posted_from': {u'$near': where}}

            #add filter to the query
            q.update(filter)

            #run the query
            events = db.objects.event.find(q)
        else:
            events = db.objects.event.find(filter)

        #perform the required sorting
        if sort == u'created':
            events.sort(u'created', direction=DESCENDING)
        elif sort == u'soon':
            events.sort(u'when', direction=DESCENDING)

        #output the results
        result = {u'events': [e[u'revision'] for e in events]}
        self.write(result)



class EventHandler(BaseHandler):

    @require_auth
    def delete(self, revision):
        '''
        Deletes an event, if the current user it that event's owner.

        TODO - enforce user restrictions
        TODO - notifications
        TODO - remove associated attendance
        '''
        obj = db.objects.event.find_one({u'revision': revision})
        if obj is None:
            raise HTTPError(404)

        db.objects.event.remove(obj[u'_id'], safe=True)
        self.finish()

    @require_auth
    def get(self, revision):
        '''
        TODO - enforce user restrictions
        '''
        #grab the event from the database
        event = db.objects.event.find_one({u'revision': revision})
        if event is None: raise HTTPError(404)

        response = {'event': event}

        #give the user the attendance info if they asked for it
        if self.request.arguments.get('attendants'):
            response['attendants'] = db.objects.attendance.find({u'event': event[u'_id']})

        self.output(response)









