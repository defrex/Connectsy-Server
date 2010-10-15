
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import json

class EventNew(ConsyTestCase):
    
    def test_event_new_validation(self):
        response = self.post('/events/', {
            u'where': 'TestCase',
            u'when': timestamp(),
            u'what': 'testing validation',
            u'broadcast': False,
        })
        self.assertEqual(response.status, 400, 'new event 400')
        
        body = response.read()
        try:
            body = json.loads(body)
        except ValueError:
            self.assertTrue(False, 'response body is json: %s' % body)
        
        self.assertTrue('error' in body)
        self.assertEqual(body['error'], 'MISSING_FIELDS')
        
    