from db import CSCursor
import db

class Model(object):
    __collection__ = None
    __fields__ = None
    
    def __init__(self, **kwargs):
        if self.__collection__ is None:
            raise AttributeError, 'Model subclasses must set __collection__'
        
        self.__original__ = kwargs
        # all models get id, but shoudn't have to add it themselves
        self.__fields__[u'id'] = None
        for key in kwargs:
            if self.__fields__.__hasattr__(key):
                self.__fields__[key] = kwargs[key]
    
    def save(self, safe=False):
        id = str(self.collection().save(self.__fields__, safe=safe))
        if id is not None:
            self.__fields__[u'id'] = id
    
    def collection(self):
        return db.objects.__getattr__(self.__collection__)
    
    @staticmethod
    def get(cls, q):
        result = db.objects.users.find_one(q)
        if result is None:
            return None
        else:
            return cls(**result)
    
    @staticmethod
    def find(cls, **query):
        cursor = db.objects.__getattr__(cls.__collection__).find(query)
        return ModelCursor(cursor, cls)
    
    # dict-like methods:
    def __len__(self):
        return len(self.__fields__)
    
    def __getitem__(self, key):
        return self.__fields__[key]
    
    def __setitem__(self, key, value):
        self.__fields__[key] = value

    def __delitem__(self, key):
        self.__fields__[key] = None
    
    def __contains__(self, key):
        return self.__fields__.__contains__(key)

class ModelCursor(CSCursor):
    
    def __init__(self, cursor, model_class):
        self.model_class = model_class
    
    def next(self, *args, **kwargs):
        result = super(ModelCursor, self).next(self, *args, **kwargs)
        return self.model_class(**result)