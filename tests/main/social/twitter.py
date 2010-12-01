
from tests.base_testcase import ConsyTestCase
import json

class Twitter(ConsyTestCase):
    
    def test_twitter(self):
        response = self.get('/social/twitter/%s/' % self.get_user()[u'username'])
        self.assertEqual(response.status, 404)
        
        response = self.put('/social/twitter/%s/' % self.get_user()[u'username'],
                             {u'token': u'faketoken', u'secret': u'fakesecret'})
        self.assertEqual(response.status, 201)
        
        response = self.get('/social/twitter/%s/' % self.get_user()[u'username'])
        self.assertEqual(response.status, 200)
        
        response = json.loads(response.read())
        self.assertTrue(u'token' in response, 'response contains token')
        self.assertTrue(u'secret' in response, 'response contains token')
        
        response = self.delete('/social/twitter/%s/' % self.get_user()[u'username'])
        self.assertEqual(response.status, 200)
        
        response = self.get('/social/twitter/%s/' % self.get_user()[u'username'])
        self.assertEqual(response.status, 404)
        
