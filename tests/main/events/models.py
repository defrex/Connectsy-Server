
from tests.base_testcase import ConsyTestCase

class EventModel(ConsyTestCase):
    
    def test_model_exists(self):
        from api.events.models import Event
        from db.models import Model
        self.assertTrue(Model in Event.__bases__)
    
    def test_event_fields(self):
        from api.events.models import Event
        
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
        from api.events.models import Event
        self.assertEquals(Event.__collection__, 'event')