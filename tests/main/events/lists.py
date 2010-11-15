
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
        
        self.follow(user, user2, reciprocal=True)
        self.follow(user3, user, reciprocal=True)
        
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
            u'what': 'user3 created',
            u'broadcast': False,
            u'creator': user3[u'username'],
        })
        event2.save()
        Attendant(user=user[u'id'], event=event2[u'id'], 
                  status=status.ATTENDING).save()
        
        event3 = Event(**{
            u'where': 'test',
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
        
        response = self.get('/events/?filter=invited')
        self.assertEqual(response.status, 200, 'response OK')
        
        events = json.loads(response.read())[u'events']
        
        self.assertEqual(len(events), 3, 'correct number of events returned')
        self.assertTrue(event1[u'revision'] in events, 'event 1 returned')
        self.assertTrue(event2[u'revision'] in events, 'event 2 returned')
        self.assertTrue(event3[u'revision'] in events, 'event 3 returned')
    
    
    def test_event_list_sort(self):
        t1 = timestamp()
        t2 = timestamp()
        t3 = timestamp()
        
        e1 = Event(**{
            u'when': t1,
            u'what': 'user2 created, broadcast',
            u'broadcast': True,
            u'creator': self.get_user()[u'username'],
            u'created': t1,
        })
        e1.save()
        
        e2 = Event(**{
            u'when': t2,
            u'what': 'user2 created, broadcast',
            u'broadcast': True,
            u'creator': self.get_user()[u'username'],
            u'created': t3,
        })
        e2.save()
        
        e3 = Event(**{
            u'when': t2,
            u'what': 'user2 created, broadcast',
            u'broadcast': True,
            u'creator': self.get_user()[u'username'],
            u'created': t2,
        })
        e3.save()
        
        e4 = Event(**{
            u'when': t3,
            u'what': 'user2 created, broadcast',
            u'broadcast': True,
            u'creator': self.get_user()[u'username'],
            u'created': t1,
        })
        e4.save()
        
        response = self.get('/events/?sort=soon&filter=creator&'
                            'username=%s' % self.get_user()[u'username'])
        self.assertEqual(response.status, 200, 'response OK')
        
        events = json.loads(response.read())[u'events']
        self.assertEqual(len(events), 4, 'correct number of events returned')
        
        self.assertEqual(events[0], e1[u'revision'], 
                         'event 1 when correct, primary sort')
        self.assertEqual(events[1], e3[u'revision'], 
                         'event 3 when correct, secondary sort')
        self.assertEqual(events[2], e2[u'revision'], 
                         'event 2 when correct, secondary sort')
        self.assertEqual(events[3], e4[u'revision'], 
                         'event 4 when correct, primary sort')



