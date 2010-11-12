
from tests.base_testcase import ConsyTestCase
from api.SMS.sms_utils import normalize_phone_number

class PhoneUtils(ConsyTestCase):
    
    def test_phone_number_notmalization(self):
        result = '16477005290'
        
        self.assertEqual(normalize_phone_number('+16477005290'), result, '+1')
        self.assertEqual(normalize_phone_number('6477005290'), result, 'no 1')
        self.assertEqual(normalize_phone_number('647.700.5290'), result, 
                         'bad chars')
        
        
    
        
