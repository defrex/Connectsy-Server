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
        result = {u'attendants': {}, u'timestamp': timestamp()}
        until = self.get_argument('until', default=None)
        #silly way of avoiding missed changes due to race conditions
        if until is not None:
            until -= 5000 
        
        #base query
        atts = db.objects.attendance.find({u'event': event_id})
        
        #handle until
        if until: atts = atts.where('timestamp > ' % until)
        
        #grab user and status from each attendance objects
        for att in atts:
            result[u'attendants'][att[u'user']] = att[u'status']
        
        self.write(result)
        
    @require_auth
    def post(self, event_id):
        '''
        Updates an invitee's attendance
        '''
        body = self.body_dict()
        
        # create a list of acceptable statuses
        valid_statuses = [v for k, v in status.__dict__.iteritems() if k[0] != '_']
        
        #make sure status is present and a correct value
        if body.get(u'status') not in valid_statuses:
            raise HTTPError(400)
        
        user = {u'user': self.get_session()[u'username']}
            
        # We want to overwrite the previous user object, but we can
        # actually share the modification code, since everything but
        # the user id and event is changing.
        att = db.objects.attendance.find_one(user) or user
        att[u'timestamp'] = timestamp()
        att[u'status']    = body[u'status']
        att[u'event']     = event_id
        db.objects.attendance.insert(att)
        
        # Hooray!
        self.finish()
    




