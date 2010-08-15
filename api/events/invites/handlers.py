from tornado.web import HTTPError

import db
from api.events.attendance import status
from utils import timestamp, require_auth
from base_handlers import BaseHandler

class InvitesHandler(BaseHandler):
    '''
    Manages invites
    '''
    
    @require_auth
    def post(self, event_id):
        #make sure the client is the event's owner
        event = db.objects.event.find_one(event_id)
        
        if not event[u'creator'] == self.get_session()[u'username']:
            raise HTTPError(403)
            
        #make sure the request has the correct info in the body
        body = self.body_dict()
        if not body or not u'users' in body:
            raise HTTPError(400)
        users = body[u'users']
        
        #make sure the event
        if event is None:
            raise HTTPError(404)
            
        #grab the existing attendance
        attendance = db.objects.attendance.find({u'event': event_id})
        
        #only create new attendances for people who weren't already there
        for att in attendance:
            #man, hash tables sure are lovely for avoiding O(n^2) runtimes...
            if att[u'username'] in users:
                del users[att[u'username']]
                
        #prevent people from inviting themselves
        if event[u'creator'] in users:
            del users[event[u'creator']]
        
        #build out the new attendance objects
        for username in users:
            db.objects.attendance.insert({u'username': username,
                    u'event': event_id, u'timestamp': timestamp(),
                    u'status': status.INVITED})
        
