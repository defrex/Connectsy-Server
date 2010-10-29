from tests.base_testcase import ConsyTestCase

class UserModel(ConsyTestCase):
    
    def test_user_model_friends(self):
        user = self.get_user()
        user2 = self.make_user(username='user2')
        user3 = self.make_user(username='user3')
        
        response = self.post('/users/%s/friends/' % user2[u'username'])
        self.assertEqual(response.status, 200, 'friend request 1')
        response = self.post('/users/%s/friends/' % user[u'username'],
                             auth_user=user2)
        self.assertEqual(response.status, 200, 'friend confirmation 1')
        
        response = self.post('/users/%s/friends/' % user[u'username'], 
                             auth_user=user3)
        self.assertEqual(response.status, 200, 'friend request 2')
        response = self.post('/users/%s/friends/' % user3[u'username'])
        self.assertEqual(response.status, 200, 'friend confirmation 2')
        
        users = user.friends()
        
        self.assertTrue(user2[u'username'] in users, 'from side friending')
        self.assertTrue(user3[u'username'] in users, 'to side friending')
        


        
