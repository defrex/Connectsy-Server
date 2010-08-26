'''
These methods are called when objects are returned from the database, based
on the name used in winter.

The object passed will be at the most recent winter revision.
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

def friend(obj):
    del obj[u'_id']
    return obj
    
def comment(obj):
    obj[u'id'] obj[u'_id']
    del obj[u'_id']
    del obj['nonce']
    del obj['event']
    return obj