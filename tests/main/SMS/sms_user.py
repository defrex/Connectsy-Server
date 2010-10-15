
from api.users.models import User
from tests.base_testcase import ConsyTestCase

class SMSUser(ConsyTestCase):
    
    def test_sms_user_creation(self):
        registered_user = User(username='smstestuser',
                               password='password',
                               number='+16666666666')
        registered_user.save()
        
        number = '+15555555555'
        name = 'Testy Smoth'
        
        user = User(number=number, display_name=name)
        
        self.assertEqual(user[u'number'], number)
        self.assertEqual(user[u'display_name'], name)
        self.assertEqual(user[u'username'], None)
        
        user.save()
        
        self.assertEqual(user[u'number'], number)
        self.assertEqual(user[u'display_name'], name)
        self.assertEqual(user[u'username'], None)
        
        got_user = User.get({u'number':number})
        
        self.assertEqual(got_user[u'number'], number)
        self.assertEqual(got_user[u'display_name'], name)
        self.assertEqual(got_user[u'username'], None)
