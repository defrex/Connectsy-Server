
from tests.base_testcase import ConsyTestCase
import json

class UserSearch(ConsyTestCase):
    
    def test_user_search(self):
        user = self.make_user(username='abc')
        user2 = self.make_user(username='cde')
        user3 = self.make_user(username='fgh')
        
        response = self.get('/users/?q=c')
        self.assertEqual(response.status, 200, 'user search request')
        
        users = json.loads(response.read())
        
        self.assertEqual(len(users), 2, '2 users returned')
        self.assertTrue(user[u'username'] in users, 'user 1 returned')
        self.assertTrue(user2[u'username'] in users, 'user 2 returned')
