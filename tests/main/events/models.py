
from tests.base_testcase import ConsyTestCase
from api.events.models import Event

class EventModel(ConsyTestCase):
    
    def test_model_exists(self):
        from db.models import Model
        self.assertTrue(Model in Event.__bases__)
    
    def test_event_fields(self):
        
        self.assertTrue(u'where' in Event.__fields__)
        self.assertTrue(u'when' in Event.__fields__)
        self.assertTrue('what' in Event.__fields__)
        self.assertTrue('broadcast' in Event.__fields__)
        self.assertTrue(u'posted_from' in Event.__fields__)
        self.assertTrue(u'location' in Event.__fields__)
        self.assertTrue(u'category' in Event.__fields__)
        self.assertTrue(u'creator' in Event.__fields__)
        self.assertTrue(u'created' in Event.__fields__)
        self.assertTrue(u'revision' in Event.__fields__)
    
    def test_event_collection(self):
        self.assertEquals(Event.__collection__, 'event')
    
    def test_event_revisioning(self):
        e = Event(broadcast=True, 
                  what='This is a test',
                  creator=self.get_user()[u'username'])
        self.assertEqual(e[u'revision'], None, 'unsaved event has no revision')
        
        e.save()
        
        self.assertTrue(e[u'revision'] is not None, 'saving creates revision')
        
        old_rev = e[u'revision']
        e[u'what'] = 'This is an edit'
        e.save()
        
        self.assertTrue(e[u'revision'] != old_rev, 'edits create new revisions')
        
        