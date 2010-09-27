import uuid
from tornado.web import HTTPError

import status
import db
from utils import timestamp, require_auth
from base_handlers import BaseHandler

class AttendanceHandler(BaseHandler):
    @require_auth
    def get(self, event_id):
        '''
        Gets a list of changes, optionally up to a certain point
        
        TODO - verify that the user is invited to this event
        '''
        result = {u'attendants': [], u'timestamp': timestamp()}
        until = self.get_argument('until', default=None)
        #silly way of avoiding missed changes due to race conditions
        if until is not None:
            until -= 5000 
        
        #base query
        atts = db.objects.attendance.find({u'event': event_id})
        
        #handle until
        if until: atts = atts.where('timestamp > ' % until)
        
        #grab user and status from each attendance objects
        tmp = {}
        for att in atts: tmp[att[u'username']] = att[u'status']
        
        result[u'attendants'] = [{'username': k, 'status': v} for k, v in tmp.iteritems()]
        
        self.write(result)
        
    @require_auth
    def post(self, event_id):
        '''
        Updates an invitee's attendance
        '''
        body = self.body_dict()
        username = self.get_session()[u'username']
        
        #make sure the event exists
        event = db.objects.event.find_one(event_id)
        if not event:
            raise HTTPError(404)
            
        #try to grab the user's existing attendance status
        att = db.objects.attendance.find_one({u'event': str(event['_id']),
                u'username': username})
                
        #if the user isn't invited, we need to error out if broadcast is off
        if att is None:
            if event[u'broadcast']:
                att = {u'username': username, u'event': event_id}
            else:
                raise HTTPError(403)
        
        # create a list of acceptable statuses
        valid_statuses = [v for k, v in status.__dict__.iteritems() if k[0] != '_']
        
        #make sure status is present and a correct value
        if body.get(u'status') not in valid_statuses:
            raise HTTPError(400)
            
        #update or create the attendance status
        att[u'timestamp'] = timestamp()
        att[u'status']    = body[u'status']
        db.objects.attendance.save(att)

        # Hooray!
        self.finish()
    




