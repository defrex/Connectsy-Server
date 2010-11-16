
from api.users.models import User
from db.models import Model
from utils import timestamp
import uuid

class Comment(Model):
    __collection__ = 'event'
    __fields__ = {
        u'nonce': uuid.uuid1(),
        u'comment': None,
        u'event': None,
        u'user': None,
        u'created': lambda: timestamp(),
    }

    def __init__(self, **kwargs):
        if u'username' in kwargs:
            kwargs[u'user'] = User.get({u'username': kwargs[u'username']})[u'id']
        super(Comment, self).__init__(**kwargs)
    
