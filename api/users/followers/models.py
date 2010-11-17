
from api.users.models import User
from db.models import Model, ModelCursor
from utils import timestamp


class FollowerCursor(ModelCursor):
    
    def followers(self, users=True):
        usernames = [f[u'follower'] for f in self]
        if users:
            return User.find({u'username': {u'$in': usernames}})
        else:
            return usernames
    
    def followees(self, users=True):
        usernames = [f[u'followee'] for f in self]
        if users:
            return User.find({u'username': {u'$in': usernames}})
        else:
            return usernames


class Follower(Model):
    __collection__ = 'followers'
    __model_cursor__ = FollowerCursor
    __fields__ = {
        u'follower': None,
        u'followee': None,
        u'created': lambda: timestamp(),
    }
    
    



