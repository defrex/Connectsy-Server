from api.events.attendance import status
from api.users.models import User
from db.models import Model, ModelCursor
from utils import timestamp


class AttendantCursor(ModelCursor):
    
    def usernames(self):
        ids = [a[u'id'] for a in self]
        users = User.find({u'_id': {'$in': ids}})
        usernames = [u[u'username'] for u in users]
        return usernames


class Attendant(Model):
    __collection__ = 'attendance'
    __model_cursor__ = AttendantCursor
    __fields__ = {
        u'status': status.INVITED,
        u'timestamp': timestamp(),
        u'event': None,
        u'user': None,
    }
    
    def __init__(self, username=None, number=None, **kwargs):
        if username:
            kwargs[u'user'] = User.get(username=username)[u'id']
        elif number:
            kwargs[u'user'] = User.get(number=number)[u'id']
        super(Attendant, self).__init__(**kwargs)
    
    def save(self, *args, **kwargs):
        if not u'id' in self:
            att = Attendant.get({u'event': self[u'event'], 
                                 u'user': self[u'user']})
            if att is not None:
                self[u'id'] = att[u'id']
        super(Attendant, self).save(*args, **kwargs)

    


