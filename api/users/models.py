from api.SMS.sms_utils import normalize_phone_number
from db.models import Model
from hashlib import sha256
from utils import timestamp
import settings
import uuid

class User(Model):
    __collection__ = 'user'
    __fields__ = {
        u'username': None,
        u'password': None,
        u'number': None,
        u'display_name': None,
        u'revision': lambda: uuid.uuid1().hex,
        u'created': lambda: timestamp(),
    }
    
    def is_registered(self):
        return self[u'username'] is not None

    def followers(self, users=False):
        from api.users.followers.models import Follower
        return Follower.find({u'followee': 
                              self[u'username']}).followers(users=users)

    def following(self, users=False):
        from api.users.followers.models import Follower
        return Follower.find({u'follower': 
                              self[u'username']}).followees(users=users)
    
    @classmethod
    def value_sanitizer(cls, field, value):
        if field == u'username' and type(value) in (str, unicode):
            return value.lower()
        elif field == u'contact_number':
            return normalize_phone_number(value)
        else:
            return value
    
    @classmethod
    def hash_password(cls, password):
        return sha256(password+settings.SALT).hexdigest()
    


