'''
These methods are called when objects are returned from the database, based
on the name used in Winter.

The object passed will be at the most recent Winter revision.
'''
def session(obj):
    return obj

def event(obj):
    obj[u'id'] = str(obj[u'_id'])
    del obj[u'_id']
    
    return obj
    
def attendance(obj):
    del obj[u'timestamp']
    del obj[u'_id']
    
    return obj
    
def user(obj):
    del obj[u'password']
    del obj[u'_id']

    return obj
