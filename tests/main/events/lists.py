
from api.events.attendance import status
from api.events.attendance.models import Attendant
from api.events.models import Event
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import json

class EventLists(ConsyTestCase):
    
    def test_event_list_invited(self):
        user = self.get_user()
        user2 = self.make_user(username='user2')
        user3 = self.make_user(username='user3')
        
        self.friend(user, user2)
        self.friend(user3, user)
        
        event1 = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'user2 created',
            u'broadcast': False,
            u'posted_from': [37.422834216666665, -122.08536667833332],
            u'creator': user2[u'username'],
        })
        event1.save()
        Attendant(user=user[u'id'], event=event1[u'id']).save()
        
        event2 = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'user3 created',
            u'broadcast': False,
            u'creator': user3[u'username'],
        })
        event2.save()
        Attendant(user=user[u'id'], event=event2[u'id'], 
                  status=status.ATTENDING).save()
        
        event3 = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'user2 created, broadcast',
            u'broadcast': True,
            u'posted_from': [37.422834216666665, -122.08536667833332],
            u'creator': user2[u'username'],
        })
        event3.save()
        
        event4 = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'user3 created',
            u'broadcast': False,
            u'creator': user3[u'username'],
        })
        event4.save()
        
        response = self.get('/events/?filter=invited&'
                            'lat=37.42283421666234&'
                            'lng=-122.0853666783334&')
        self.assertEqual(response.status, 200, 'response OK')
        
        events = json.loads(response.read())[u'events']
        
        self.assertEqual(len(events), 3, 'correct number of events returned')
        self.assertTrue(event1[u'revision'] in events, 'event 1 returned')
        self.assertTrue(event2[u'revision'] in events, 'event 2 returned')
    




