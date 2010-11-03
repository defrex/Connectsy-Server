
from db.models import Model
from tests.base_testcase import ConsyTestCase

        
class MyModel(Model):
    '''
    The model used for model testing
    '''
    __collection__ = 'test_collection'
    __fields__ = {
        u'testfield': None,
    }
    
    @classmethod
    def value_sanitizer(cls, field, value):
        return value.lower()


class DBModels(ConsyTestCase):
    
    def test_model_field_sanitization(self):
        
        data = MyModel(testfield='TestFieldValue')
        data.save()
        
        self.assertEqual(data[u'testfield'], 'testfieldvalue', 
                         'sanitize on save')
        
        db_data = MyModel.get({u'testfield': 'TestfieldValue'})
        
        self.assertTrue(db_data is not None, 'sanitize queries')
        
        self.assertEqual(db_data[u'testfield'], 'testfieldvalue', 
                         'sanitized in the db')
        
        db_data2 = MyModel.get(db_data[u'id'])
        
        self.assertTrue(db_data2 is not None, 'id query works')
        
        db_data3 = MyModel.find({u'testfield': {'$in': ['TESTfieldValue',
                                                        'ADASDF',
                                                        'someothervalue']}})
        
        self.assertEqual(len(db_data3), 1, 'complex queries work')
        
        db_data3 = MyModel.find({u'testfield': {'$in': ['TESTfieldValue',
                                                        'ADASDF',
                                                        'someothervalue']}})
    
    def test_model_init(self):
        
        data = MyModel(testfield='value')
        self.assertEqual(data[u'testfield'], 'value', 'value correctly set')
        
        data2 = MyModel(testfield='value')
        data2.save()
        self.assertEqual(data2[u'testfield'], 'value', 'value correctly set')
    

