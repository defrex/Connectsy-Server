from api.events.attendance.models import Attendant
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth
import db
import status


class AttendanceHandler(BaseHandler):
    @require_auth
    def get(self, event_id):
        '''
        Gets a list of changes, optionally up to a certain point
        
        TODO - verify that the user is invited to this event
        '''
        atts = Attendant.find({u'event': event_id})
        retts = []
        for att in atts:
            user = att.user()
            ret = {'status': att[u'status'],
                   'user_id': user[u'id']}
            if user.is_registered():
                ret[u'username'] = user[u'username']
            else:
                ret[u'display_name'] = user[u'display_name']
            retts.append(ret)
        self.write({u'attendants': retts})
    
    @require_auth
    def post(self, event_id):
        '''
        Updates an invitee's attendance
        '''
        body = self.body_dict()
        username = self.get_session()[u'username']
        
        #make sure the event exists
        event = db.objects.event.find_one(event_id)
        if not event: raise HTTPError(404)
        
        #try to grab the user's existing attendance status
        att = Attendant.get({u'event': str(event['_id']),
                u'username': username})
        
        #if the user isn't invited, we need to error out if broadcast is off
        if att is None:
            if event[u'broadcast']:
                att = Attendant(username=username, event=event_id)
            else:
                raise HTTPError(403)
        
        # create a list of acceptable statuses
        valid_statuses = [v for k, v in status.__dict__.iteritems() if k[0] != '_']
        
        #make sure status is present and a correct value
        if body.get(u'status') not in valid_statuses:
            raise HTTPError(400)
        
        att[u'status'] = body[u'status']
        att.save()

        # Hooray!
        self.finish()
    




