
from api.events.attendance import status
from api.events.attendance.models import Attendant
from api.events.models import Event
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import json

class EventAttendants(ConsyTestCase):
    
    def test_attendants_with_event(self):
        event = Event(broadcast=True, 
                  what='This is a test',
                  creator=self.get_user()[u'username'])
        event.save()
        
        att_user = self.make_user('att_user')
        Attendant(**{
            u'status': status.ATTENDING,
            u'timestamp': timestamp(),
            u'event': event[u'id'],
            u'user': att_user[u'id'],
        }).save()
        
        response = self.get('/events/%s/?attendants=true' % event[u'revision'])
        self.assertEqual(response.status, 200, 'event get success')
        
        body = json.loads(response.read())
        
        self.assertTrue(u'attendants' in body, 'response has attendants')
        self.assertEqual(len(body['attendants']), 1, 'event has 1 attendant')
        
        self.assertTrue(u'username' in body['attendants'][0], 'att has username')
        self.assertTrue(u'user' in body['attendants'][0], 'att has user id')
        self.assertTrue(u'event' in body['attendants'][0], 'att has event')
        self.assertTrue(u'status' in body['attendants'][0], 'att has status')
        self.assertTrue(u'timestamp' in body['attendants'][0], 'att has timestamp')
        
        for k, v in body['attendants'][0].iteritems():
            self.assertTrue(v is not None, '%s is not None' % k)
    
        
        
    