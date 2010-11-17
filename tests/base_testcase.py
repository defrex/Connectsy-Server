
from api.users.followers.models import Follower
from api.users.models import User
from db import objects
from db.index_setup import indexes
from httplib import HTTPConnection
from unittest2 import TestCase
from urllib import urlencode
from utils import timestamp
import db
import json
import settings
import uuid
import winter


class ConsyTestCase(TestCase):
    
    def flush_db(self):
        dbase = db.objects.get_database()
        for c in winter.managers:
            dbase.drop_collection(c)
            dbase.create_collection(c)
        # gotta write to disk to prevent inconsistent test failure due to 
        # missing collections
        db.objects.connection['admin'].command('fsync')
    
    def setUp(self):
        self.flush_db()
        
        # Set up the indexes
        for collection in indexes:
            l = [(field, direction) for field, direction in 
                 indexes[collection].iteritems()]
            objects[collection].ensure_index(l)
    
#    def tearDown(self):
#        self.flush_db()
    
    def request(self, method, path, body=None, headers=dict(), auth=True, 
                auth_user=None):
        if type(body) == dict:
            body = json.dumps(body)
        
        if auth:
            auth_user = auth_user or self.get_user()
            headers['Authenticate'] = 'Token auth=%s' % self.get_token(user=auth_user)
        
        con = HTTPConnection('localhost:%i' % settings.PORT)
        con.request(method, path, body, headers)
        return con.getresponse()
    
    def get(self, path, args=None, auth=True, auth_user=None):
        if args is None:
            return self.request('GET', path, auth=auth, auth_user=auth_user)
        else:
            urlargs = '?'
            for key, val in args.iteritems():
                urlargs += '%s=%s&' % (key, val)
            return self.request('GET', path+urlargs, auth=auth, 
                                auth_user=auth_user)
    
    def post(self, path, body=None, args=None, auth=True, auth_user=None):
        headers = {}
        if args is not None:
            if body is not None:
                raise TypeError, 'args overwrites body in post'
            body = urlencode(args)
            headers["Content-type"] = "application/x-www-form-urlencoded"
        
        return self.request('POST', path, body, headers=headers, auth=auth, 
                            auth_user=auth_user)
    
    def put(self, path, body=None, auth=True, auth_user=None):
        return self.request('PUT', path, body, auth=auth, auth_user=auth_user)
    
    def delete(self, path, body=None, auth=True, auth_user=None):
        return self.request('DELETE', path, body, auth=auth, auth_user=auth_user)
    
    def get_token(self, user=None):
        if not user:
            user = self.get_user()
        token = str(db.objects.session.insert({
            u'timestamp': timestamp(),
            u'username': user[u'username'],
        }))
        return token
    
    def get_user(self):
        if not hasattr(self, '__user__'):
            self.__user__ = self.make_user()
        return self.__user__
    
    __user_number__ = 0
    def make_user(self, username=None):
        if username is None:
            self.__user_number__ += 1
            username = 'testuser%i' % self.__user_number__
        u = User(**{
                u'username': username, 
                u'password': 'passw0rd',
                u'number': '+16656656665',
                u'revision': uuid.uuid1().hex,
                u'created': timestamp(),
            })
        u.save()
        return u
    
    def follow(self, follower, followee, reciprocal=False):
        f = Follower(follower=follower[u'username'],
                     followee=followee[u'username'])
        f.save()
        if reciprocal:
            f2 = Follower(follower=followee[u'username'],
                          followee=follower[u'username'])
            f2.save()
            return f, f2
        else:
            return f



