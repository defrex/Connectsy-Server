
from api.SMS.models import SMSRegister
from api.events.attendance import status
from api.events.attendance.models import Attendant
from api.events.comments.models import Comment
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
        
        smsuser = User(number='+16475555555', display_name='Testy Smoth')
        smsuser.save()
        
        Attendant(user=user[u'id'], event=event[u'id']).save()
        
        SMSRegister(contact_number=smsuser[u'number'], 
                    twilio_number=settings.TWILIO_NUMBERS[0], 
                    event=event[u'id'], 
                    expires=event[u'when'],
                    user=user[u'id']).save()
        
        return user, event, smsuser
    
    def test_sms_reply_who(self):
        if not settings.TEST_SMS: return
        
        user, event, smsuser = self.prep_for_response_sms()
        response = self.post('/extras/SMS/', args={'From': smsuser[u'number'],
                                                   'To': settings.TWILIO_NUMBERS[0],
                                                   'Body': '#who'})
        self.assertEqual(response.status, 200)
    
    def test_sms_reply_what(self):
        if not settings.TEST_SMS: return
        
        user, event, smsuser = self.prep_for_response_sms()
        response = self.post('/extras/SMS/', args={'From': smsuser[u'number'],
                                                   'To': settings.TWILIO_NUMBERS[0],
                                                   'Body': '#what'})
        self.assertEqual(response.status, 200)
        
    
    def test_sms_reply_in(self):
        if not settings.TEST_SMS: return
        
        user, event, smsuser = self.prep_for_response_sms()
        
        att = Attendant.get({u'user': user[u'id'], u'event': event[u'id']})
        self.assertEqual(att[u'status'], status.INVITED, 'user is invited')
        
        response = self.post('/extras/SMS/', args={'From': smsuser[u'number'],
                                                   'To': settings.TWILIO_NUMBERS[0],
                                                   'Body': '#in'})
        self.assertEqual(response.status, 200)
        
        att = Attendant.get({u'user': user[u'id'], u'event': event[u'id']})
        self.assertEqual(att[u'status'], status.ATTENDING, 'user is attending')
        
    
    def test_sms_reply_comment(self):
        if not settings.TEST_SMS: return
        
        user, event, smsuser = self.prep_for_response_sms()
        
        comment = 'This is a comment'
        
        response = self.post('/extras/SMS/', args={'From': smsuser[u'number'],
                                                   'To': settings.TWILIO_NUMBERS[0],
                                                   'Body': comment})
        self.assertEqual(response.status, 200)
        
        db_comment = Comment.get({'event': event[u'id']})
        
        self.assertNotEqual(db_comment, None, 'Comment exists')
        self.assertEqual(comment, db_comment[u'comment'], 'comment body matches')
        
    

