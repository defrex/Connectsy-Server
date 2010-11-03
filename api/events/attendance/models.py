from api.events.attendance import status
from api.users.models import User
from db.models import Model, ModelCursor
from pymongo.objectid import ObjectId
from utils import timestamp


class AttendantCursor(ModelCursor):
    
    def usernames(self):
        ids = [ObjectId(a[u'user']) for a in self]
        users = User.find({u'_id': {u'$in': ids}})
        usernames = [u[u'username'] for u in users if u[u'username'] is not None]
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
            kwargs[u'user'] = User.get({u'username': username})[u'id']
        elif number:
            kwargs[u'user'] = User.get({u'number': number})[u'id']
        super(Attendant, self).__init__(**kwargs)
    
    def user(self):
        return User.get(self[u'user'])
    
    @classmethod
    def get(cls, q):
        if u'username' in q:
            q[u'user'] = User.get({u'username': q[u'username']})[u'id']
            del q[u'username']
        return super(Attendant, cls).get(q)
    
    @classmethod
    def to_notify(cls, event, skip=list()):
        atts = cls.find({u'event': event[u'id'], u'status': status.ATTENDING})
        ids = [ObjectId(a[u'user']) for a in atts]
        users = User.find({u'_id': {u'$in': ids}})
        ret = [event[u'creator']]
        for u in users:
            if u[u'username'] is not None:
                ret.append(u[u'username'])
            else:
                ret.append(u[u'id'])
        ret = [u for u in ret if u not in skip]
        return ret
    
    def save(self, *args, **kwargs):
        if not u'id' in self:
            print 'looking for upsert id'
            att = Attendant.get({u'event': self[u'event'], 
                                 u'user': self[u'user']})
            if att is not None:
                self[u'id'] = att[u'id']
        super(Attendant, self).save(*args, **kwargs)

    


