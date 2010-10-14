
from tests.base_testcase import ConsyTestCase

class ServerRunning(ConsyTestCase):
    
    def test_server_running(self):
        response = self.get('/', auth=False)
        self.assertEqual(response.status, 200)
