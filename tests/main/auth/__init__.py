
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import json

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
        