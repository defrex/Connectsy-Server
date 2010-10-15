
from api import SMS
from api.SMS.models import SMSRegister
from api.events.models import Event
from api.users.models import User
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import settings

class SMSReply(ConsyTestCase):
    
    def prep_for_response_sms(self):
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
        
        smsuser = User(number='+15555555555', display_name='Testy Smoth')
        smsuser.save()
        
        SMSRegister(contact_number=smsuser[u'number'], 
                    twilio_number=settings.TWILIO_NUMBERS[0], 
                    event=event[u'id'], 
                    expires=event[u'when'],
                    user=user[u'id']).save()
        
        return user, event, smsuser
    
    def test_sms_reply_who(self):
        user, event, smsuser = self.prep_for_response_sms()
        response = self.post('/extra/SMS/', args={'From': smsuser[u'number'],
                                                  'To': settings.TWILIO_NUMBERS[0],
                                                  'Body': '#who'})
        self.assertEqual(response.status, 200)
        
        
        
