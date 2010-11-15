
from api.events.attendance.models import Attendant
from tests.base_testcase import ConsyTestCase
import json

class EventInvites(ConsyTestCase):
    
    def test_auto_invite(self):
        user = self.get_user()
        user2 = self.make_user()
        
        self.follow(user2, user)
        
        response = self.post('/events/', {
            u'broadcast': True,
            u'what': 'Testin event creation',
        })
        self.assertEqual(response.status, 201, 'new event 201')
        event = json.loads(response.read())
        
        att = Attendant.get({u'event': event[u'id'], u'user': user2[u'id']})
        
        self.assertNotEqual(att, None, 'user auto-invited')
        
    
    def test_new_event_invite(self):
        user = self.get_user()
        user2 = self.make_user()
        
        self.follow(user2, user)
        
        response = self.post('/events/', {
            u'broadcast': False,
            u'what': 'Testin event creation',
            u'users': [user2[u'username']],
        })
        self.assertEqual(response.status, 201, 'new event 201')
        event = json.loads(response.read())
        
        att = Attendant.get({u'event': event[u'id'], u'user': user2[u'id']})
        
        self.assertNotEqual(att, None, 'user auto-invited')
        
    