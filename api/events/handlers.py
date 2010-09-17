import uuid
from tornado.web import HTTPError
from pymongo import DESCENDING, GEO2D

import db
from utils import timestamp, require_auth
from base_handlers import BaseHandler
from api.users.friends import status as friend_status

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
        #grab the sorting/filtering types from the args
        sort = self.get_argument('sort', None)
        filter = self.get_argument('filter', None)
        
        #set up the base query
        if sort is None or sort == u'nearby':
            #grab lat/lng from the query, defaulting to toronto
            lat = float(self.get_argument('lat', '43.652527'))
            lng = float(self.get_argument('lng', '-79.381961'))
            where = [lat, lng]
            events = db.objects.event.find({u'posted_from': {u'$near': where}})
            sort = sort or 'soon'
        else:
            events = db.objects.event.find()
        
        #perform filtering
        if filter == 'friends':
            #todo
        #any other value for filter is a category
        elif filter:
            events = events.where({u'category', filter})
        
        #perform the required sorting
        if sort == u'created':
            events = events.sort(u'created', direction=DESCENDING)
        elif sort == u'soon':
            events = events.sort(u'when', direction=DESCENDING)
            
        
            
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
        
    






