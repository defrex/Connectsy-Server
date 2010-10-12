import hashlib

from tornado.web import HTTPError

import settings

# Normalized json import.  You should only use this for decoding, and use
# json_encoder for encoding.
try:    import simplejson as json
except: import json
# Note that we try to import simplejson first.  This is because simplejson
# can optionally use a compiled C module that's much faster than the native
# Python implementation.  The json module included with 2.6 lacks this
# feature.

# Use this for all your json encoding needs.  It will automatically
# handle sanitization, and plays nicely with cursors from the DB.
from json_encoder import json_encoder #convoluted, but avoids a circular import

# Timestamp generation
import time
def timestamp():
    return int(time.time()*1000)

from datetime import datetime
def from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp/1000)

# Generates a salted SHA1 hash of the specified value
def hash(val):
    h = hashlib.sha1(val)
    h.update(settings.SALT)
    return h.hexdigest()
    

# Decorator for methods that require user authorization.  If the user
# specified a valid token in the request, the method will be called as per
# usual.  If the token was invalid in any way (missing, malformed, expired, etc)
# a proper Http401 will be returned to the client.
def require_auth(f):
    def sub(self, *args, **kwargs):
        if not self.get_session():
            #i'm not sure if this works if we raise errors... but i guess
            #it doesn't hurt to set it -- the spec requires it
            self.set_header('WWW-Authenticate', 'Token');
            raise HTTPError(401)
        return f(self, *args, **kwargs)
    return sub

def format_date(date):
    pass
