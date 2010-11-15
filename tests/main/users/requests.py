
from tests.base_testcase import ConsyTestCase

class UserRequests(ConsyTestCase):
    
    def test_user_requests_get(self):
        user = self.make_user()
        
        response = self.get('/users/%s/' % user[u'username'])
        self.assertEqual(response.status, 200, 'user GET 200')
