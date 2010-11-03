
from api.users.models import User
from tests.base_testcase import ConsyTestCase

class Authentication(ConsyTestCase):
    
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
    
