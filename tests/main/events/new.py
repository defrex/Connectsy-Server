
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import json

class ServerRunning(ConsyTestCase):
    
    def test_event_new_validation(self):
        response = self.post('/events/', {
            u'where': 'TestCase',
            u'when': timestamp(),
            u'what': 'testing validation',
            u'broadcast': False,
        })
        self.assertEqual(response.status, 400, 'new event 400')
        
        body = json.loads(response.read())
        
        self.assertTrue('error' in body)
        
    