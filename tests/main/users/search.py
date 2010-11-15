
from tests.base_testcase import ConsyTestCase

class UserSearch(ConsyTestCase):
    
    def test_user_search(self):
        user = self.make_user(username='abc')
        user2 = self.make_user(username='cde')
        user3 = self.make_user(username='fgh')
        
        response = self.get('/users/?q=c')
        self.assertEqual(response.status, 200, 'user search request')
