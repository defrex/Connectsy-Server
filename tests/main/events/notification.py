
from api.events.attendance import status
from api.events.attendance.models import Attendant
from api.events.models import Event
from tests.main.notification.bases import GenericPollNotificationTest
from utils import timestamp

class EventNotifications(GenericPollNotificationTest):
    
    def test_event_new_notification(self):
        
        to_invite = self.make_user(username='noticeuser')
        
        self.register_for_notifications(user=to_invite)
        
        event = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'test',
            u'broadcast': False,
            u'posted_from': [37.422834216666665, -122.08536667833332],
            u'creator': self.get_user()[u'username'],
        })
        event.save()
        
        response = self.post('/events/%s/invites/' % event[u'id'], 
                             {'users': [to_invite[u'username']]})
        self.assertEqual(response.status, 200, 'user invited')
        
        nots = self.get_new_notifications(user=to_invite)
        
        self.assertEqual(len(nots), 1, 'one new notification')
        
        notification = nots[0]
        
        self.assertTrue(u'event_revision' in notification, 
                        'poll response has event rev')
        
        self.assertEqual(notification[u'event_revision'], event[u'revision'], 
                         'event has the corrrect revision')
        
    
    def test_event_comment_notification(self):
        
        to_notify = self.make_user(username='noticeuser')
        
        self.register_for_notifications(user=to_notify)
        
        event = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'test',
            u'broadcast': False,
            u'posted_from': [37.422834216666665, -122.08536667833332],
            u'creator': self.get_user()[u'username'],
        })
        event.save()
        
        Attendant(**{
            u'status': status.ATTENDING,
            u'timestamp': timestamp(),
            u'event': event[u'id'],
            u'user': to_notify[u'id'],
        }).save()
        
        comment = 'the test comment'
        
        response = self.post('/events/%s/comments/' % event[u'id'], 
                             {'comment': comment})
        self.assertEqual(response.status, 200, 'comments POST 200')
        
        nots = self.get_new_notifications(user=to_notify)
        
        self.assertEqual(len(nots), 1, 'one new notification')
        
        notification = nots[0]
        
        self.assertTrue(u'type' in notification, 
                        'poll response has type')
        self.assertEqual(notification[u'type'], 'comment', 
                         'event has the correct type')
        
        self.assertTrue(u'event_revision' in notification, 
                        'poll response has event rev')
        self.assertEqual(notification[u'event_revision'], event[u'revision'], 
                         'event has the correct revision')
        
        self.assertTrue(u'comment' in notification, 
                        'poll response has comment')
        self.assertEqual(notification[u'comment'], comment, 
                         'event has the correct comment')
        
        self.assertTrue(u'commenter' in notification, 
                        'poll response has commenter')
        self.assertEqual(notification[u'commenter'], self.get_user()[u'username'], 
                         'event has the correct commenter')
        
    
    def test_event_attending_notification(self):
        
        to_notify = self.make_user(username='noticeuser')
        to_attend = self.make_user(username='attending_user')
        
        self.register_for_notifications(user=to_notify)
        
        event = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'test',
            u'broadcast': False,
            u'posted_from': [37.422834216666665, -122.08536667833332],
            u'creator': self.get_user()[u'username'],
        })
        event.save()
        
        # user getting the notification needs to be attending
        Attendant(**{
            u'status': status.ATTENDING,
            u'timestamp': timestamp(),
            u'event': event[u'id'],
            u'user': to_notify[u'id'],
        }).save()
        
        # this attendant will trigger the notification
        Attendant(**{
            u'status': status.INVITED,
            u'timestamp': timestamp(),
            u'event': event[u'id'],
            u'user': to_attend[u'id'],
        }).save()
        
        response = self.post('/events/%s/attendants/' % event[u'id'], 
                             {u'status': status.ATTENDING}, 
                             auth_user=to_attend)
        self.assertEqual(response.status, 200, 'attendants POST 200')
        
        nots = self.get_new_notifications(user=to_notify)
        
        self.assertEqual(len(nots), 1, 'one new notification')
        
        notification = nots[0]
        
        self.assertTrue(u'type' in notification, 
                        'poll response has type')
        self.assertEqual(notification[u'type'], 'attendant', 
                         'event has the correct type')
        
        self.assertTrue(u'event_revision' in notification, 
                        'poll response has event rev')
        self.assertEqual(notification[u'event_revision'], event[u'revision'], 
                         'event has the corrrect revision')
        
        self.assertTrue(u'attendant' in notification, 
                        'poll response has attendant')
        self.assertEqual(notification[u'attendant'], to_attend[u'username'], 
                         'event has the corrrect attendant')
        
    
    def test_event_notification_attending_creator(self):
        
        to_attend = self.make_user(username='attending_user')
        
        self.register_for_notifications(user=self.get_user())
        
        event = Event(**{
            u'where': 'test',
            u'when': timestamp(),
            u'what': 'test',
            u'broadcast': False,
            u'posted_from': [37.422834216666665, -122.08536667833332],
            u'creator': self.get_user()[u'username'],
        })
        event.save()
        
        # this attendant will trigger the notification
        Attendant(**{
            u'status': status.INVITED,
            u'timestamp': timestamp(),
            u'event': event[u'id'],
            u'user': to_attend[u'id'],
        }).save()
        
        response = self.post('/events/%s/attendants/' % event[u'id'], 
                             {u'status': status.ATTENDING}, 
                             auth_user=to_attend)
        self.assertEqual(response.status, 200, 'attendants POST 200')
        
        nots = self.get_new_notifications(user=self.get_user())
        
        self.assertEqual(len(nots), 1, 'one new notification')
        
        notification = nots[0]
        
        self.assertTrue(u'type' in notification, 
                        'poll response has type')
        self.assertEqual(notification[u'type'], 'attendant', 
                         'event has the correct type')
        
        self.assertTrue(u'event_revision' in notification, 
                        'poll response has event rev')
        self.assertEqual(notification[u'event_revision'], event[u'revision'], 
                         'event has the corrrect revision')
        
        self.assertTrue(u'attendant' in notification, 
                        'poll response has attendant')
        self.assertEqual(notification[u'attendant'], to_attend[u'username'], 
                         'event has the corrrect attendant')
        
        
        
    