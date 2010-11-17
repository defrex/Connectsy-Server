from api.users.models import User
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import timestamp
import db



class TokenHandler(BaseHandler):
    def get(self):        
        #ensure that username and password are in the args
        self.require_args('username', 'password')
        
        username = self.get_argument(u'username').lower()
        password = User.hash_password(self.get_argument('password'))
        user = User.get({u'username': username,  u'password': password})
        
        if user is None: raise HTTPError(404)
        
        #otherwise generate a token, save it, and return it
        token = str(db.objects.session.insert({
            u'timestamp': timestamp(),
            u'username': username
        }))
        self.write(token)
    


