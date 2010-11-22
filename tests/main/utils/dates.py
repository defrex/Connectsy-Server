
from api.SMS.sms_utils import format_date
from tests.base_testcase import ConsyTestCase

class DateUtils(ConsyTestCase):
    
    def test_sms_date_format(self):
        timestamp = 1240443127965
        result = 'Apr. 22, 2009 at 7:32PM'
        
        self.assertEqual(format_date(timestamp), result, "no 0 in time")
        
    
        
