from api.events.attendance.models import Attendant
from api.events.models import Event
from api.users.models import User
from base_handlers import BaseHandler
from pymongo import DESCENDING
from pymongo.objectid import ObjectId
from tornado.web import HTTPError
from utils import timestamp, require_auth
import db
import re
import uuid


# Events occuring more than UNTIL_LIMIT milliseconds from now won't
# be displayed
UNTIL_LIMIT = 1000 * 60 * 60 * 24 * 30 # 30d
# Events occuring more than SINCE_LIMIT millie seconds before now
# won't be displayed
SINCE_LIMIT = 1000 * 60 * 60 * 24 * 10 # 10d

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
        event = Event()

        #grab data from the user-supplied dict
        try:
            event[u'creator'] = self.get_session()[u'username']
            event[u'what'] = req_body[u'what']
            event[u'broadcast'] = req_body[u'broadcast']
            
            #optional:
            event[u'where'] = req_body.get(u'where')
            event[u'when'] = req_body.get(u'when')
            event[u'posted_from'] = req_body.get(u'posted_from')
            event[u'location'] = req_body.get(u'location')
            event[u'category'] = req_body.get(u'category')
            event[u'client'] = req_body.get(u'client')
        except KeyError, e:
            self.output({'error': 'MISSING_FIELDS',
                         'field_missing': e[0]}, 400)
        else:
            event.save()

            response[u'revision'] = event[u'revision']
            response[u'id'] = event[u'id']
            
            self.output(response, 201)

    @require_auth
    def get(self):
        '''
        Gets a list of events
        '''
        #store username for later use
        username = self.get_session()[u'username']
        user = User.get({u'username': username})

        #grab the sorting/filtering types from the args
        #funky names avoid conflict with python builtins
        q_sort = self.get_argument(u'sort', u'nearby')
        q_filter = self.get_argument(u'filter', None)
        category = self.get_argument(u'category', None)
        
        if not q_filter in (u'invited', u'creator', u'public'):
            raise HTTPError(404)

        #prep the geospatial info
        lat = float(self.get_argument('lat', '43.652527'))
        lng = float(self.get_argument('lng', '-79.381961'))
        where = [lat, lng]

        #prep filtering
        if q_filter == 'invited':
            event_ids = [ObjectId(att[u'event']) for att in 
                         Attendant.find({u'user': user[u'id']})]
            q_filter = {u'_id': {'$in': event_ids}}
        elif q_filter == u'creator':
            q_filter = {u'creator': self.get_argument(u'username', username)}
        elif q_filter == u'public':
            q_filter = {u'broadcast': True}
            if category is not None:
                q_filter[u'category'] = category 
        
        # Limit to nearby times
        q_filter.update({u'when': {u'$lt': timestamp() + UNTIL_LIMIT,
            u'$gt': timestamp() - SINCE_LIMIT}})
        
        # Handle geo sorting
        if q_sort == u'nearby':
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
        event = Event.get({u'revision': revision})
        if event is None: raise HTTPError(404)
        
        response = {'event': event.as_dict()}

        #give the user the attendance info if they asked for it
        if self.request.arguments.get('attendants'):
            response['attendants'] = [a.as_dict() for a in 
                                      Attendant.find({u'event': event[u'id']})]

        self.output(response)









