
from httplib import HTTPConnection
from unittest2 import TestCase
import db
import json
import settings


class ConsyTestCase(TestCase):
    
    def flush_db(self):
        db.objects.reconnect()
        db.objects.connection.drop_database(db.objects.get_database())
        db.objects.reconnect()
    
    def setUp(self):
        self.flush_db()
    
    def tearDown(self):
        self.flush_db()
    
    def request(self, method, path, body=None, auth=True):
        if type(body) == dict:
            body = json.dumps(body)
        
        if auth:
            headers = {'Authenticate': 'Token token=%s' % self.get_token()}
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
    
    def post(self, path, body=None, auth=True):
        return self.request('POST', path, body, auth=auth)
    
    def put(self, path, body=None, auth=True):
        return self.request('PUT', path, body, auth=auth)
    
    def delete(self, path, body=None, auth=True):
        return self.request('DELETE', path, body, auth=auth)
    
    def get_token(self):
        response = self.put('/users/testuser/', {
            u'password': u'password',
            u'number': u'+15555555555',
        }, auth=False)
        assert response.status == 201
        response = self.get('/token/', {
            u'password': u'password',
            u'username': u'testuser',
        }, auth=False)
        return response.read()

