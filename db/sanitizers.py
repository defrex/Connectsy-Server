'''
These methods are called when objects are returned from the database, based
on the name used in winter.

The object passed will be at the most recent winter revision.
'''

from datetime import datetime

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
    obj[u'id'] = obj[u'_id']
    del obj[u'_id']
    del obj['event']
    return obj
    
def notification_reg(obj):
    return obj
    
def sms_reg(obj):
    obj[u'id'] = str(obj[u'_id'])
    del obj[u'_id']
    obj[u'expires'] = datetime.fromtimestamp(obj[u'expires'])
    return obj
