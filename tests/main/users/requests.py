
from tests.base_testcase import ConsyTestCase
import json

class UserRequests(ConsyTestCase):
    
    def test_user_requests_get(self):
        user = self.make_user()
        
        response = self.get('/users/%s/' % user[u'username'])
        self.assertEqual(response.status, 200, 'user GET 200')
        user = json.loads(response.read())
        
        self.assertTrue(u'username' in user, 'response has username')
        self.assertTrue(u'created' in user, 'response has created')
        self.assertTrue(u'id' in user, 'response has id')
