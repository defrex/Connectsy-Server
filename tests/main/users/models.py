from api.users.models import User
from tests.base_testcase import ConsyTestCase

class UserModel(ConsyTestCase):
    
    def test_user_model_init(self):
        username = u'test_username'
        user = User(username=username)
        self.assertEqual(user[u'username'], username, 'username correctly set')
        


        
