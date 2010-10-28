
from tests.main.notification.bases import GenericPollNotificationTest

class UserFriending(GenericPollNotificationTest):
    
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
        

        
