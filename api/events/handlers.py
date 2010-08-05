import uuid
from tornado.web import HTTPError

import db
from utils import timestamp, require_auth
from base_handlers import BaseHandler

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
            event[u'posted_from'] = req_body[u'posted_from']
            if u'category' in req_body:
                event[u'category'] = req_body[u'category']
            else:
                event[u'category'] = ''
        except KeyError:
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
        result = {u'events': [e[u'revision'] for e in db.objects.event.find()]}
        #events = self.db.events.find()
        #for event in [e['revision'] for e in events]:
        #    result['events'].append(event)
        self.write(result)



class EventHandler(BaseHandler):
    
    @require_auth
    def delete(self, revision):
        '''
        Deletes an event, if the current user it that event's owner.
        
        TODO - enforce user restrictions
        TODO - notifications
        '''
        obj = db.objects.event.find_one({u'revision': revision})
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
            response['attendants'] = db.attendance.find({u'event': event[u'_id']})
        
        self.output(response)
        
    






