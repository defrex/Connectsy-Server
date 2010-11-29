
from api.SMS.models import SMSRegister
from tests.base_testcase import ConsyTestCase
import settings

class SMSRegistration(ConsyTestCase):
    
    def test_sms_registration(self):
        if not settings.TEST_SMS: return
        
        number = u'11111111111'
        
        response = self.post('/events/', {
            u'broadcast': True,
            u'what': 'Testin',
            u'timezone': 'Etc/UTC',
            u'contacts': [{u'name': u't1', u'number': number}]
        })
        self.assertEqual(response.status, 201, 'new event 201')
        
        response = self.post('/events/', {
            u'broadcast': True,
            u'what': 'Testin',
            u'timezone': 'Etc/UTC',
            u'contacts': [{u'name': u't1', u'number': number}]
        })
        self.assertEqual(response.status, 201, 'new event 201')
        
        sms_reg = SMSRegister.find({u'contact_number': number})
        
        self.assertEqual(len(sms_reg), 2, "2 numbers registered")
        
        self.assertNotEqual(sms_reg[0][u'twilio_number'], 
                            sms_reg[1][u'twilio_number'], 
                            'different twillio numbers')
    
    def test_sms_registration_over(self):
        if not settings.TEST_SMS: return
        
        number = u'11111111111'
        
        for i in range(0, len(settings.TWILIO_NUMBERS)):
            response = self.post('/events/', {
                u'broadcast': True,
                u'what': 'Testin',
                u'timezone': 'Etc/UTC',
                u'contacts': [{u'name': u't%i' % i, u'number': number}]
            })
            self.assertEqual(response.status, 201, 'new event 201')
        
        response = self.post('/events/', {
            u'broadcast': True,
            u'what': 'Testin',
            u'timezone': 'Etc/UTC',
            u'contacts': [{u'name': u'tx', u'number': number}]
        })
        self.assertEqual(response.status, 409, 'out of numbers')
        
