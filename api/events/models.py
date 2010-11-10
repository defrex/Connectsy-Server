
from api.events.attendance.models import Attendant
from db.models import Model
from utils import timestamp
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
        u'created': timestamp(),
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
    