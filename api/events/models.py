
from api import SMS
from api.events.attendance.models import Attendant
from api.users.models import User
from db.models import Model
from utils import timestamp
import notifications
import pytz
import uuid

class Event(Model):
    __collection__ = 'event'
    __fields__ = {
        u'where': None,
        u'when': None,
        u'what': None,
        u'posted_from': None,
        u'location': None,
        u'creator': None,
        u'category': None,
        u'broadcast': False,
        u'created': lambda: timestamp(),
        u'revision': None,
    }
    
    def save(self, *args, **kwargs):
        self[u'revision'] = uuid.uuid1().hex
        super(Event, self).save(*args, **kwargs)

    def user_can_access(self, user):
        if user[u'username'] == self[u'creator']:
            return True
        if not self[u'broadcast']:
            att = Attendant.get({u'event': self[u'id'], 
                                 u'user': user[u'id']})
            return att is not None
        return True
    
    def invite(self, usernames=None, contacts=None, tz=None):
        if usernames is not None:
            #prevent people from inviting themselves
            if self[u'creator'] in usernames:
                usernames.remove(self[u'creator'])
            # convert usernames to user objects
            users = list(User.find({u'username': {'$in': usernames}}))
        else:
            users = list()
        ret = None
        if contacts is not None:
            registered, out_of_numbers, has_username = SMS.register(self, 
                    contacts, tz=tz)
            users += has_username
            users += [reg for reg in registered if reg not in users]
            if len(out_of_numbers) > 0:
                ret = out_of_numbers
        
        for user in users:
            Attendant(user=user[u'id'], event=self[u'id']).save()
            #send the invite notification
            if user[u'username'] is not None: name = user[u'username']
            else: name = user[u'id']
            
            notifications.send(name, {u'type': 'invite', 
                                      u'event_revision': self[u'revision'],
                                      u'event_id': self[u'id']})
        return ret
        
    
