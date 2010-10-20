from UserDict import DictMixin
from copy import copy
from db import CSCursor
from pymongo.objectid import ObjectId
import db



class ModelCursor(CSCursor):
    
    def __new__(cls, cursor, model_class):
        # All your interitance heirarchy are belong to us
        cursor.__class__ = cls
        return cursor
    
    def __init__(self, cursor, model_class):
        self.model_class = model_class
    
    def next(self, *args, **kwargs):
        result = super(ModelCursor, self).next(*args, **kwargs)
        return self.model_class(**result)


class Model(object, DictMixin):
    __model_cursor__ = ModelCursor
    __collection__ = None
    __fields__ = None
    
    def __init__(self, **kwargs):
        if self.__collection__ is None:
            raise AttributeError, 'Model subclasses must set __collection__'
        if self.__class__.__fields__ is None:
            raise AttributeError, 'Model subclasses must set fields'
        self.__original__ = kwargs
        self.__data__ = copy(self.__class__.__fields__)
        # all models get id, but shoudn't have to add it themselves
        self.__data__[u'id'] = None
        for key in kwargs:
            if key in self.__data__:
                self.__data__[key] = kwargs[key]
        if u'_id' in kwargs and self.__data__[u'id'] is None:
            self.__data__[u'id'] = str(kwargs[u'_id'])
    
    def save(self, safe=False):
        obj = copy(self.__data__)
        if obj[u'id'] is not None:
            obj[u'_id'] = ObjectId(obj[u'id'])
            del obj[u'id']
        id = self.collection().save(obj, safe=safe)
        if id is not None:
            self[u'id'] = str(id)
    
    def collection(self):
        return db.objects.__getattr__(self.__collection__)
    
    def repr(self):
        return '%s: %s' % (self.__class__, str(self.__data__))
    
    @classmethod
    def get(cls, q):
        result = db.objects.__getattr__(cls.__collection__).find_one(q)
        if result is None:
            return None
        else:
            return cls(**result)
    
    @classmethod
    def find(cls, q):
        cursor = db.objects.__getattr__(cls.__collection__).find(q)
        return cls.__model_cursor__(cursor, cls)
    
    def __getattr__(self, name):
        if name == '__fields__':
            raise AttributeError(name)
    
    # dict-like methods:
    def __len__(self):
        return len(self.__data__)
    
    def __getitem__(self, key):
        return self.__data__[key]
    
    def __setitem__(self, key, value):
        self.__data__[key] = value

    def __delitem__(self, key):
        self.__data__[key] = None
    
    def keys(self):
        return self.__data__.keys()
    
    def __contains__(self, key):
        return self.__data__.__contains__(key)
    
    def __iter__(self, *args, **kwargs):
        return self.__data__.__iter__(*args, **kwargs)
    
    def iteritems(self, *args, **kwargs):
        return self.__data__.iteritems(*args, **kwargs)
    


