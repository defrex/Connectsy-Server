
from tornado.web import HTTPError
from utils import json, json_encoder
import db
import settings
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    
    def output(self, obj, status=200):
        '''
        Sets up the request to return JSON, writes the supplied object to
        the response as JSON (accounting for PyMongo and sanitizing, and
        finishes the request.
        '''
        self.set_status(status)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        op = json_encoder(obj)
        #if settings.DEBUG: print op
        self.write(op)
        self.finish()
    
    def created(self, obj=None):
        '''
        Finishes the request, telling the user that something was successfully
        created.
        '''
        self.set_status(201)
        self.finish()
    
    def get_session(self):
        '''
        Returns the session object for the token attached to the request, or
        None if no token was attached or the token is invalid.
        '''
        #attempt to use the cached session
        if hasattr(self, 'session'):
            return self.session
            
        #try to grab the token from the request
        token = self.request.headers.get('Authenticate')
        if token is None: return None
        
        #strip leading 'Token auth='
        prefix = 'Token auth='
        if not token.startswith(prefix): 
            return None
        token = token[len(prefix):]
        
        #fetch the session from the database, and cache it
        self.session = db.objects.session.find_one(token)
        
        #only perform the following validations if the session actually exists
        if self.session:
            #TODO - if the session has expired, raise the appropriate error
            pass
            
        return self.session
        
    def get_user(self):
        '''
        Returns the user that made this request, based on the token used in the request.  If
        no token was attached, or the token was invalid, returns None.
        '''
        #late import to break the cycle
        from api.users.models import User
        session = self.get_session()
        return session and User.get({u'username': session[u'username']})
    
    def require_args(self, *args):
        '''
        Ensures that the argument names passed to the function are preset
        in the request GET or POST parameters.  If any arguments are missing
        an Http400 error will be raised, with a message body specifying
        the missing arguments.
        '''
        missing = []
        for arg in filter(lambda a: not a in self.request.arguments, args):
            missing.append(arg)
            
        if len(missing) > 0:
            error = u'Missing arguments:\n\n'
            for arg in missing:
                error += u'%s\n' % arg
            raise HTTPError(400, error)
            
    def body_dict(self):
        '''
        Parses the request body as JSON, and returns the dict representation
        '''
        #memoize
        if hasattr(self, '_body_dict'):
            return self._body_dict
            
        try:
            self._body_dict = json.loads(self.request.body)
            return self._body_dict
        except Exception, e:
            raise HTTPError(400, e.args[0])
        
