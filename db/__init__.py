# We're avoiding the json import in utils due to circular import issues
try: import simplejson as json
except: import json

from pymongo import Connection
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.objectid import ObjectId

import winter
import settings
import migrations #triggers winter migration setup
import sanitizers

class CSObject(dict):
    # We can't do our crazy monkey patching here, because
    # heap types (dict being one of them) can't have their __class__
    # changed.
    
    def __init__(self, obj, type):
        self._objtype = type
        #clone the values
        self.update(obj)

    def sanitize(self):
        '''
        Attempts to run the sanitizer.  If no sanitizer is defined, the
        sanitization process is skipped.  In either case, returns a the
        object dictionary.
        '''
        #melt the snow
        if '_winter' in self:
            del self['_winter']
        
        if hasattr(sanitizers, self._objtype):
            return getattr(sanitizers, self._objtype)(self)
        return self

class CSCursor(Cursor):
    '''
    This object assumed that the collection it's working on exists under
    the corresponding name in winter's migration system.
    
    I'm not going to bother documenting this, because it's too meta
    for words to describe better than code.
    '''
    def __new__(cls, cursor):
        # All your interitance heirarchy are belong to us
        cursor.__class__ = cls
        return cursor
        
    def __init__(self, cursor):
        pass #override parent's init
        
    def next(self, *args, **kwargs):
        result = Cursor.next(self, *args, **kwargs)
        if not result is None:
            return CSObject(getattr(winter.objects, self.collection.name)(result),
                    self.collection.name)
        return result
        
class CSCollection(Collection):
    '''
    This object assumed that the collection it's working on exists under
    the corresponding name in winter's migration system.
    
    I'm not going to bother documenting this, because it's too meta
    for words to describe better than code.
    '''
    
    def __new__(cls, collection):
        # All your interitance heirarchy are belong to us
        collection.__class__ = cls
        return collection
        
    def __init__(self, collection):
        pass #override parent's init
    
    # Overridden methods for automatically handling winter migrations
    
    def find_one(self, *args, **kwargs):
        result = Collection.find_one(self, *args, **kwargs)
        if not result is None:
            return CSObject(getattr(winter.objects, self.name)(result), self.name)
        return result

    def find(self, *args, **kwargs):
        #if it's a single argument and a string, convert it to an objectid
        if len(args) == 1 and isinstance(args[0], basestring):
            args = ({u'_id': ObjectId(args[0])},)
            
            
        result = Collection.find(self, *args, **kwargs)
        return CSCursor(result)
       
class CSConnection(object):
    '''
    The grand management singleton for Connectsy's database connection(s).
    '''
    
    #singleton -- __getattr__ doesn't work on modules, so this is as
    #good as it gets
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CSConnection, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance
        
    def __init__(self, dbname, host='127.0.0.1', port=27017):
        self.dbname = dbname
        self.connection = Connection(host=host, port=port)
    
    def get_database(self, dbname=None):
        dbname = dbname or self.dbname
        return self.connection[dbname]
    
    def __getattr__(self, obj):
        #try to use winter
        if obj in winter.objects:
            return CSCollection(self.get_database()[obj])
        else:
            #trust me, you want this here.
            raise Exception('No collection "%s" registered with winter' % obj)
        
class CSEncoder(json.JSONEncoder):
    '''
    Custom JSON encoder that properly handles PyMongo cursors and CSObjects.
    '''
    
    # We have to override this, because it thinks CSObjects are
    # just plain dicts, which will prevent use from otherwise
    # sanitizing them.
    def encode(self, o):
        self._walk(o)
        return json.JSONEncoder.encode(self, o)
        
    def _walk(self, o):
        '''
        Walks the object heirarchy, sanitizing any CSObjects
        '''
        if isinstance(o, CSObject):
            o.sanitize()
        elif isinstance(o, dict):
            for item in o.itervalues():
                self._walk(item)
    
    def default(self, o):
        if isinstance(o, Cursor):
            return [i for i in o]
        elif isinstance(o, ObjectId):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)
            
# This is where it all comes together.  Use db.objects to get at your
# collections, just like you would with a standard PyMongo database object.
# The extra twist is that winter migrations are automatically applied to
# any object being removed from the database.  Similarly, all objects
# coming out of the database become a subtype of dict, with the added
# 'sanitize' method, which will return a sanitized version of the object
# based on sanitizers defined in sanitizers.py.
objects = CSConnection(settings.DB_NAME, settings.DB_HOST, settings.DB_PORT) 

# Run the index setup file.
import index_setup
    