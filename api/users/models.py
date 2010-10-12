from db.models import Model
from utils import timestamp
import uuid

class User(Model):
    __collection__ = 'user'
    
    __fields__ = {
        u'username': None,
        u'password': None,
        u'number': None,
        u'display_name': None,
        u'revision': uuid.uuid1().hex,
        u'created': timestamp(),
    }
    
    def is_registered(self):
        return self[u'username'] is not None

        
        


