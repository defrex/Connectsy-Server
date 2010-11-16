
from api.events.models import Event
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import json

class EventNew(ConsyTestCase):
    
    def test_event_new_validation(self):
        response = self.post('/events/', {
            u'where': 'TestCase',
            u'when': timestamp(),
            u'broadcast': False,
        })
        self.assertEqual(response.status, 400, 'new event 400')
        body = json.loads(response.read())
        self.assertEqual(body['error'], 'MISSING_FIELDS')
        self.assertEqual(body['field'], 'what')
        
        response = self.post('/events/', {
            u'what': 'TestCase',
            u'where': '--------------------------', #len: 26
        })
        self.assertEqual(response.status, 400, 'new event 400')
        body = json.loads(response.read())
        self.assertEqual(body['error'], 'FIELD_LENGTH')
        self.assertEqual(body['field'], 'where')
        
        response = self.post('/events/', {
            u'what': '-------------------------'
                     '-------------------------'
                     '-------------------------'
                     '-------------------------'
                     '-------------------------'
                     '----------------', #len: 141
        })
        self.assertEqual(response.status, 400, 'new event 400')
        body = json.loads(response.read())
        self.assertEqual(body['error'], 'FIELD_LENGTH')
        self.assertEqual(body['field'], 'what')
    
    def test_event_new(self):
        response = self.post('/events/', {
            u'broadcast': True,
            u'what': 'Testin event creation',
        })
        self.assertEqual(response.status, 201, 'new event 201')
        
        body = response.read()
        try:
            body = json.loads(body)
        except ValueError:
            self.assertTrue(False, 'response body is json: %s' % body)
        
        response = self.get('/events/%s/' % body[u'revision'])
        self.assertEqual(response.status, 200, 'get event 200')
        
        body = response.read()
        try:
            body = json.loads(body)
        except ValueError:
            self.assertTrue(False, 'response body is json: %s' % body)
        
        self.assertEqual(len(body['event']), 6, 
                         'correct number of fields returned')
    
    def test_event_new_created(self):
        response = self.post('/events/', {
            u'broadcast': True,
            u'what': 'Testin event creation',
        })
        self.assertEqual(response.status, 201, 'new event 201')
        
        response = self.post('/events/', {
            u'broadcast': True,
            u'what': 'Testin event creation',
        })
        self.assertEqual(response.status, 201, 'new event 201')
        
        events = Event.find({u'creator': self.get_user()[u'username']})
        self.assertEqual(len(events), 2, '2 events created')
        self.assertNotEqual(events[0][u'created'], events[1][u'created'], 
                            'created times are different')
        
        
        
        
    