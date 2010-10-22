
from api.events.comments.models import Comment
from api.events.models import Event
from api.users.models import User
from tests.base_testcase import ConsyTestCase
from utils import timestamp
import json

class EventComments(ConsyTestCase):
    
    def test_new_comment(self):
        user = User(username='event_creator',
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
        
        comment = 'the test comment'
        
        post = self.post('/events/%s/comments/' % event[u'id'], 
                             {'comment': comment})
        
        self.assertEqual(post.status, 200, 'comment POST 200')
        
        get = self.get('/events/%s/comments/' % event[u'id'])
        
        self.assertEqual(get.status, 200, 'comment GET 200')
        
        try:
            get = json.loads(get.read())
        except ValueError:
            self.assertTrue(False, 'comment GET not JSON')
        
        self.assertTrue('comments' in get, 'comment GET has comments')
        self.assertEqual(len(get['comments']), 1, 'comment GET return 1 '
                         'comment')
        self.assertTrue('comment' in get['comments'][0], 'comment GET has '
                        'comments')
        self.assertEqual(get['comments'][0]['comment'], comment, 'comment GET '
                         'returned the right comment')
        self.assertTrue('username' in get['comments'][0], 
                        'comment GET has username')
        self.assertFalse('display_name' in get['comments'][0], 
                        'comment GET does not have display_name')
        
    def test_sms_comment(self):
        display_name = 'Test User display'
        user = User(number='+16666666666', 
                    display_name=display_name)
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
        
        comment = 'the test comment'
        
        Comment(**{
            u'comment': comment,
            u'event': event[u'id'],
            u'user': user[u'id']
        }).save()
        
        get = self.get('/events/%s/comments/' % event[u'id'])
        
        self.assertEqual(get.status, 200, 'comment GET 200')
        
        try:
            get = json.loads(get.read())
        except ValueError:
            self.assertTrue(False, 'comment GET not JSON')
        
        self.assertTrue('comments' in get, 
                        'comments returned')
        self.assertEqual(len(get['comments']), 1, 
                         'correct number of comments')
        
        self.assertFalse('username' in get['comments'][0], 
                        'username field unavailable')
        self.assertTrue('display_name' in get['comments'][0], 
                        'display_name field available')
        self.assertEqual(get['comments'][0]['display_name'], display_name, 
                         'display_name field set correctly')
        
        
        
    