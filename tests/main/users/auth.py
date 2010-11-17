
from api.users.models import User
from httplib import HTTPConnection
from tests.base_testcase import ConsyTestCase
import settings

class Authentication(ConsyTestCase):
    
    def test_bad_token(self):
        con = HTTPConnection('localhost:%i' % settings.PORT)
        con.request('GET', '/users/%s/' % self.get_user()[u'username'], 
                    None, {'Authenticate': 'Token auth=tokenfail'})
        response = con.getresponse()
        self.assertEqual(response.status, 401, '401 on bad token')
    
    def test_registration(self):
        response = self.put('/users/testuser/', {
            u'password': u'password',
            u'number': u'+16747005290',
        }, auth=False)
        self.assertEqual(response.status, 201, 'Registration PUT')
        response = self.get('/token/', {
            u'password': u'password',
            u'username': u'testuser',
        }, auth=False)
        self.assertEqual(response.status, 200, 'Registered user /token/ GET '
                         'returns 200')
        self.assertTrue(len(response.read()) > 0, 'Registered user /token/ GET '
                         'returns a token')
    
    
    def test_registraction_username_validation(self):
        User(**{
            u'username': u'test',
            u'password': u'passw0rd',
            u'number': u'16475557000',
        }).save()
        
        response = self.put('/users/test/', {
            u'password': u'passw0rd',
            u'number': u'+16747005290',
        }, auth=False)
        self.assertEqual(response.status, 409, 'cannot reuse usernames')
        
        response = self.put('/users/tesT/', {
            u'password': u'passw0rd',
            u'number': u'+16747005290',
        }, auth=False)
        self.assertEqual(response.status, 409, 'usernames case insensitive')
        
    def test_case_insensitive_login(self):
        User(**{
            u'username': u'test',
            u'password': User.hash_password(u'passw0rd'),
            u'number': u'16475557000',
        }).save()
        
        response = self.get('/token/', {u'password': u'passw0rd',
                                        u'username': u'TesT'}, auth=False)
        self.assertEqual(response.status, 200, '/token/ GET')
    
