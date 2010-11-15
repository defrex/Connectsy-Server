
from tests.main.notification.bases import GenericPollNotificationTest
import json

class UserFollowing(GenericPollNotificationTest):
    
    def test_user_following(self):
        user1 = self.make_user()
        user2 = self.make_user()
        
        response = self.post('/users/%s/followers/' % user2[u'username'],
                             {'follow': True}, auth_user=user1)
        self.assertEqual(response.status, 200, 'user1 follow user2 request')
        
        response = self.get('/users/%s/followers/' % user2[u'username'])
        self.assertEqual(response.status, 200, 'get user2 followers list')
        
        followers = json.loads(response.read())
        
        self.assertEqual(len(followers), 1, 'user2 has 1 follower')
        self.assertEqual(followers[0][u'username'], user1[u'username'], 
                         'user1 is following user2')
        
        response = self.get('/users/%s/following/' % user1[u'username'])
        self.assertEqual(response.status, 200, 'get user1 followees list')
        
        followees = json.loads(response.read())
        
        self.assertEqual(len(followees), 1, 'user1 has 1 followee')
        self.assertEqual(followees[0][u'username'], user2[u'username'], 
                         'user1 is following user2')
    
    def test_user_following_notification(self):
        to_notify = self.make_user()
        self.register_for_notifications(user=to_notify)
        
        response = self.post('/users/%s/followers/' % to_notify[u'username'],
                             {'follow': True})
        self.assertEqual(response.status, 200, 'follow notify user')
        
        nots = self.get_new_notifications(user=to_notify)
        
        self.assertEqual(len(nots), 1, 'one new notification')
        
        notification = nots[0]
        
        self.assertTrue(u'type' in notification, 
                        'poll response has type')
        self.assertEqual(notification[u'type'], 'follow', 
                         'event has the correct type')
        
        self.assertTrue(u'username' in notification, 
                        'poll response has username')
        self.assertEqual(notification[u'username'], self.get_user()[u'username'], 
                         'notification has the correct username')
    

