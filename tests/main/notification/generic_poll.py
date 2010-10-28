
from tests.main.notification.bases import GenericPollNotificationTest
import notifications
import uuid

class GenericPollNotifications(GenericPollNotificationTest):
    
    def test_generic_poll_notification(self):
        
        self.register_for_notifications()
        
        notification_extra = uuid.uuid4().hex
        
        notifications.send(self.get_user()[u'username'], 
                           {u'type': 'test', u'extra': notification_extra})
        
        nots = self.get_new_notifications()
        
        self.assertEqual(len(nots), 1, 'one new notification')
        
        notification = nots[0]
        
        self.assertTrue(u'extra' in notification, 'notification has extra')
        
        self.assertEqual(notification[u'extra'], notification_extra, 
                         'notification extra matches')
        
    