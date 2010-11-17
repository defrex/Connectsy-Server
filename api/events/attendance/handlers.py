from api.events.attendance.models import Attendant
from api.events.models import Event
from api.users.models import User
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth
import notifications
import status


class AttendanceHandler(BaseHandler):
    @require_auth
    def get(self, event_id):
        event = Event.get({u'id': event_id})
        if not event: raise HTTPError(404)
        
        if not event.user_can_access(self.get_user()):
            raise HTTPError(401)
        self.output({u'attendants': Attendant.find({u'event': 
                                        event_id}).serializable(name=True)})
    
    @require_auth
    def post(self, event_id):
        '''
        Updates an invitee's attendance
        '''
        body = self.body_dict()
        username = self.get_session()[u'username']
        user = User.get({u'username': username})
        #make sure the event exists
        event = Event.get(event_id)
        if not event: raise HTTPError(404)
        
        #try to grab the user's existing attendance status
        att = Attendant.get({u'event': event[u'id'],
                             u'user': user[u'id']})
        
        #if the user isn't invited, we need to error out if broadcast is off
        if att is None:
            if event[u'broadcast']:
                att = Attendant(user=user[u'id'], event=event[u'id'])
            else:
                raise HTTPError(403)
        
        # create a list of acceptable statuses
        valid_statuses = [v for k, v in status.__dict__.iteritems() if k[0] != '_']
        
        #make sure status is present and a correct value
        if body.get(u'status') not in valid_statuses:
            raise HTTPError(400)
        
        att[u'status'] = body[u'status']
        att.save()
        
        if att[u'status'] == status.ATTENDING:
            #Send out the attendant notifications
            usernames = Attendant.to_notify(event, skip=[username])
            print 'notifying', usernames
            for uname in usernames:
                notifications.send(uname, {u'type': 'attendant',
                                           u'event_revision': event[u'revision'],
                                           u'event_id': event[u'id'],
                                           u'attendant': username})
    




