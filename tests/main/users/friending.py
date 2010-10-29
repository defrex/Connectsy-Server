
from tests.main.notification.bases import GenericPollNotificationTest

class UserFriending(GenericPollNotificationTest):
    
    def test_user_friending(self):
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
    
    
    def test_user_friend_notification(self):
        to_notify = self.make_user(username='noticeuser')
        
        self.register_for_notifications(user=to_notify)
        
        response = self.post('/users/%s/friends/' % to_notify[u'username'])
        self.assertEqual(response.status, 200, 'friended sucessfully')
        
        nots = self.get_new_notifications(user=to_notify)
        
        self.assertEqual(len(nots), 1, 'one new notification')
        
        notification = nots[0]
        
        self.assertTrue(u'type' in notification, 
                        'poll response has type')
        self.assertEqual(notification[u'type'], 'friend', 
                         'event has the correct type')
        
        self.assertTrue(u'username' in notification, 
                        'poll response has username')
        self.assertEqual(notification[u'username'], self.get_user()[u'username'], 
                         'notification has the correct username')
        

        
