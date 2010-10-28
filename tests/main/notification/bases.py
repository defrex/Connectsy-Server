
from tests.base_testcase import ConsyTestCase
import json
import uuid

class GenericPollNotificationTest(ConsyTestCase):
    
    def register_for_notifications(self, user=None):
        if not user: user = self.get_user()
        self.client_id = uuid.uuid4().hex
        
        response = self.post('/notifications/register/', {
            u'client_type': u'generic_poll',
            u'client_id': self.client_id,
        }, auth_user=user);
        
        self.assertEqual(response.status, 200, 'registered for notifications')
    
    
    def get_new_notifications(self, user=None):
        if not user: user = self.get_user()
        
        response = self.get('/notifications/poll/', 
                            {u'client_id': self.client_id}, auth_user=user)
        self.assertEqual(response.status, 200, 'notification poll success')
        
        try:
            response = json.loads(response.read())
        except ValueError:
            self.assertTrue(False, 'poll response not json')
        
        self.assertTrue(u'notifications' in response, 
                        'poll response notifications')
        
        return response[u'notifications']
        
        
    