
from api import SMS
from api.SMS.models import SMSRegister
from api.events.models import Event
from api.users.models import User
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import notifications
import settings
import uuid

class SMSNotification(ConsyTestCase):
    
    def test_sms_registration(self):
        
        number = '+15555555555'
        event_id = uuid.uuid1().hex
        
        SMSRegister(contact_number=number, 
                    twilio_number='+15555555555', 
                    event=event_id, 
                    expires=timestamp(),
                    user='notneeded').save()
        
        smsee = SMSRegister.get({u'event': event_id,
                                 u'contact_number': number})
        
        self.assertNotEqual(smsee, None)
    
    def test_sms_notification_creation(self):
        if not settings.TEST_SMS: return
        
        user = User(username='smstestuser',
                    password='password',
                    number='+16666666666')
        user.save()
        
        event = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'test',
            u'broadcast': False,
            u'posted_from': [37.422834216666665, -122.08536667833332],
            u'creator': user[u'username'],
        })
        event.save()
        
        number = '+16475551234'
        name = 'Testy Smoth'
        
        reg, out, is_user = SMS.register(event, [{u'number':number, u'name':name},
                                                 {u'number':user[u'number'], 
                                                  u'name':name}])
        
        self.assertEqual(len(reg), 1, 'correct ammout registered')
        self.assertEqual(len(out), 0, 'correct ammout out of numbers')
        self.assertEqual(len(is_user), 1, 'correct ammout are already users')
        
        reged = reg[0]
        
        self.assertEqual(reged.__class__, User)
        self.assertTrue(u'id' in reged)
        
        result = notifications.send(reged[u'id'], 
                                    {u'type': 'invite', 
                                     u'event_revision': event[u'revision'],
                                     u'event_id': event[u'id']})
        
        self.assertEqual(len(result), 1, 'the correct number of notifications '
                                         'were sent')
        self.assertTrue(result[0], 'the notification was sent correctly')
        
