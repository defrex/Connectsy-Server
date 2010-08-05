from tornado.web import HTTPError

from base_handlers import BaseHandler

import db
from utils import timestamp, hash

class TokenHandler(BaseHandler):
    def get(self):        
        #ensure that username and password are in the args
        self.require_args('username', 'password')
        
        #hash and salt the password... mmm delicious
        password = hash(self.get_argument('password'))
        
        #try to find a user with the given username/password
        user = db.objects.user.find_one({u'username': self.get_argument(u'username'),
                u'password': password})
        
        #fail if they don't exist
        if user is None: raise HTTPError(404) #FIXME: better error
        
        #otherwise generate a token, save it, and return it
        token = str(db.objects.session.insert({
            u'timestamp': timestamp(),
            u'username': self.get_argument(u'username')
        }))
        
        self.write(token)
    


