import re
import uuid
from tornado.web import HTTPError
from pymongo import DESCENDING, GEO2D
from pymongo.objectid import ObjectId
from pymongo.bson import Code

import db
from utils import timestamp, require_auth
from base_handlers import BaseHandler
from api.users.friends import status as friend_status
from api.users.friends.friend_utils import get_friends

# Events occuring more than UNTIL_LIMIT milliseconds from now won't
# be displayed
UNTIL_LIMIT = 1000 * 60 * 60 * 24 * 30 # 30d
# Events occuring more than SINCE_LIMIT millie seconds before now
# won't be displayed
SINCE_LIMIT = 1000 * 60 * 60 * 4 # 4h

# Any character matching this regex is stripped from the username
username_sanitizer = re.compile(r"\W")

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
            event[u'what'] = req_body[u'what']
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
        '''
        #store username for later use
        username = self.get_session()[u'username']

        #grab the sorting/filtering types from the args
        #funky names avoid conflict with python builtins
        q_sort = self.get_argument(u'sort', u'nearby')
        q_filter = self.get_argument(u'filter', None)

        #prep filtering
        if q_filter == 'friends':
        
            #prep the geospatial info
            lat = float(self.get_argument('lat', '43.652527'))
            lng = float(self.get_argument('lng', '-79.381961'))
            where = [lat, lng]
        
            # This is madness.
            # THIS IS CONNECTSY!
            # Here's how this mofo works:
            #
            # First, we get a list of all events started by the user's
            # friends.
            #
            # Second, we query and mapreduce the attendance collection to
            # find all unique events where the user or the user's friends
            # are attending.  These results are then split into two groups:
            #   * Events the user is invited to or attending
            #   * Events just the user's friends are invited to or attending
            #
            # NOTE: MR is used rather than an aggregation function because
            #       currently MongoDB doesn't support shareded aggregate ops.
            #
            # We then do a big query on the `event` collection that looks
            # for events from those lists using $or operators.
            #   
            #   1: User is invited to or attending event
            #   2: Event is broadcast and friend is invited/attending
            #   3: Event is broadcast and friend created it
            #
            
            # Get the user's friends
            friends = get_friends(username)
            
            # Get a list of events started by friends
            events_friends_created = [event[u'_id'] for event in \
                db.objects.event.find({u'creator': {u'$in': friends}})]

            # Add the user to the friends list, for mapreduce reasons
            friends.append(username)

            # Limit MR'd entries to those from the friends + user
            query = {
                u'username': {u'$in': friends}
            }

            # Javascript map function - takes just the event_id and username
            # from the already-filtered collection
            map_func = Code("""function() {
                  emit(this.event, {event: this.event, user: this.username});
            }""")

            # Javascript reduce function.  Returns {event_id, username}, where
            # username is a random user, or the current user if they were
            # invited to that event.  Note that this WILL include events
            # that ONLY have the user attending, and not any of his friends.
            san_username = username_sanitizer.sub('', username)
            reduce_func = Code("""function(key, values) {
                var username = values[0].user;
            
                //check to see if the user is in the list of values
                for (var i=0; i<values.length; i++)
                {
                    if (values[i].user == "%s")
                    {
                        username = "%s";
                        break;
                    }
                }
                
                return {event: key, user: username};
            }""" % (san_username, san_username)) #yeah, this is lazy...

            # Gets a Cursor to {event, user} objects containing all unique
            # events friends or the user are attending.  
            event_list = [a[u'value'] for a in db.objects.attendance.map_reduce(
                map=map_func, reduce=reduce_func, query=query).find()]
             
            # POTENTIAL OPTIMIZATION BELOW: These can be split in a single
            #   loop rather than two separate map calls, which will loop
            #   the whole list twice.
                
            # List of events the user is invited to
            events_user_invited = map(lambda a: ObjectId(a[u'event']),
                filter(lambda a: a[u'user'] == username, event_list))
            
            # List of events that the user's friends are invited to
            events_friends_invited = map(lambda a: ObjectId(a[u'event']),
                filter(lambda a: a[u'user'] != username, event_list))
            
            # Assemble the query.  Note the use of $or, which basically
            # gives us the union for free.
            q_filter = {u'$or': [
                # Events user is invited to
                {u'_id': {u'$in': events_user_invited}},
                # Broadcast events the user's friends are invited to
                {u'broadcast': True, u'_id': {u'$in': events_friends_invited}},
                # Broadcast events started by the user's friends
                {u'broadcast': True, u'_id': {u'$in': events_friends_created}},
            ]}
            
            ### FINAL RESULTS:
            # Union of the following events:
            #   All events the user is invited to
            #   All broadcast events the user's friends are invited to
            #   All broadcast events started by the user's friends
            
        # All other query types share a common base query
        else:
            #show only this user's created events
            if q_filter == u'creator':
                q_filter = {u'creator': self.get_argument(u'username', username)}
            #any other value for filter is a category
            elif q_filter:
                q_filter = {u'category': q_filter} 
            else:
                q_filter = {}
                
            #grab all the events the user's invited to
            user_invited = [ObjectId(a[u'event']) for a in \
                db.objects.attendance.find({u'username': username})]
                
            #the query
            q_filter.update({u'$or': [
                # All broadcast events
                {u'broadcast': True},
                # Events created by the user
                {u'creator': username},
                # Non-broadcast events that the user's invited to
                {u'_id': {u'$in': user_invited}},
            ]})

        # Limit to nearby times
        q_filter.update({u'when': {u'$lt': timestamp() + UNTIL_LIMIT,
            u'$gt': timestamp() - SINCE_LIMIT}})
        
        # Handle geo sorting
        if q_sort == u'nearby':
            #set up location info
            lat = float(self.get_argument('lat', '43.652527'))
            lng = float(self.get_argument('lng', '-79.381961'))
            where = [lat, lng]
            
            #set the sort
            q_filter.update({u'posted_from': {u'$near': where}})

            #use 'soon' as a secondary sort
            q_sort = u'soon'

        # Run the query
        events = db.objects.event.find(q_filter, limit=30)

        #perform the required sorting
        if q_sort == u'created':
            events.sort(u'created', direction=DESCENDING)
        elif q_sort == u'soon':
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









