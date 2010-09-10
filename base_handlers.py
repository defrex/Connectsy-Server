from os.path import join
import logging

import tornado.web
import tornado.escape
import tornado.auth
from tornado.web import HTTPError

import db
from utils import json, json_encoder
import settings

class BaseHandler(tornado.web.RequestHandler):
    
    def output(self, obj, status=200):
        '''
        Sets up the request to return JSON, writes the supplied object to
        the response as JSON (accounting for PyMongo and sanitizing, and
        finishes the request.
        '''
        self.set_status(status)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json_encoder(obj))
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
        if token:
            #strip leading 'Token '
            if not token.startswith('Token '):
                return None
            token = token[6:]
            
            #make sure the token format is correct
            if not token.startswith('auth='):
                return None
            token = token[5:]

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
        session = self.get_session()
        return session and db.objects.user.find_one({u'username': session[u'username']})
    
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
        
# Root handler
import time
start_time = time.time()
class MainHandler(BaseHandler):
    def get(self):
        version = u'0.2'
        mode = u'Development' if settings.DEVELOPMENT else u'Production'
        uptime = (time.time() - start_time) / 1000
        
        self.set_status(418)
        self.set_header('X-Server', 'Connectsy-Teapot/0.1 Freshly Brewed')
        self.set_header('Content-Type', 'text/plain; charset=UTF-8')
        self.write(u'''
        Connectsy API Server
            Version: %s
            Mode:    %s
            Uptime:  %s seconds
            
        "Everything should be made as simple as possible, but not simpler."
          -- Albert Einstein
        ''' % (version, mode, uptime))
        self.finish()



