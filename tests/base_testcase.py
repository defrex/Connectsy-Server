
from api.users.models import User
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
        for c in winter.managers:
            db.objects.get_database().drop_collection(c)
    
    def setUp(self):
        self.flush_db()
    
    def tearDown(self):
        self.flush_db()
    
    def request(self, method, path, body=None, auth=True):
        if type(body) == dict:
            body = json.dumps(body)
        
        if auth:
            headers = {'Authenticate': 'Token auth=%s' % self.get_token()}
        else:
            headers = {}
        
        con = HTTPConnection('localhost:%i' % settings.PORT)
        con.request(method, path, body, headers)
        return con.getresponse()
    
    def get(self, path, args=None, auth=True):
        if args is None:
            return self.request('GET', path, auth=auth)
        else:
            urlargs = '?'
            for key, val in args.iteritems():
                urlargs += '%s=%s&' % (key, val)
            return self.request('GET', path+urlargs, auth=auth)
    
    def post(self, path, body=None, args=None, auth=True):
        if args is not None:
            if body is not None:
                raise TypeError, 'args overwrites body in post'
            body = urlencode(args)
        return self.request('POST', path, body, auth=auth)
    
    def put(self, path, body=None, auth=True):
        return self.request('PUT', path, body, auth=auth)
    
    def delete(self, path, body=None, auth=True):
        return self.request('DELETE', path, body, auth=auth)
    
    def get_token(self):
        User(**{
            u'username': 'testuser', 
            u'password': 'password',
            u'number': '+15555555555',
            u'revision': uuid.uuid1().hex,
            u'created': timestamp(),
        }).save()
        token = str(db.objects.session.insert({
            u'timestamp': timestamp(),
            u'username': 'testuser',
        }))
        return token

