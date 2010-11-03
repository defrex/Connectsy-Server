from api.users.friends import status
from db.models import Model
from utils import timestamp
import db
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

    def friends(self):
        '''
        Gets a list of usernames of the user's friends
        '''
        to_side = [friend[u'to'] for friend in 
                    db.objects.friend.find({u'from': self[u'username'], 
                                            u'status': status.ACCEPTED})]
        from_side = [friend[u'from'] for friend in 
                    db.objects.friend.find({u'to': self[u'username'], 
                                            u'status': status.ACCEPTED})]
        return to_side + from_side
    
    @classmethod
    def value_sanitizer(cls, field, value):
        if field == u'username':
            return value.lower()
        else:
            return value
    

        


