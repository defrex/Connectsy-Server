'''
Connecty's automated test suite.  This will run through the REST API, testing
things purely from a client's perspective.

This needs to be split off into multiple files, as it's a little messy.  We
just need a clean way to share the token/auth info.

We can also add much more complete tests.  Right now these only do 'positive'
tests, but we also need to make sure that stuff that should fail, fails.
'''

from utils import json
from framework import Runner, json_body, status_is

# Some constants we'll need throughout the tests
username = 'testuser1'
password = 'foo'
token = None # This gets filled in later.  It's kind of an ugly hack :(

# Generates appropriate auth headesr
def auth():
    return {'Authenticate': 'Token %s' % token}
    
def require_keys(body, *args):
    keys = body.keys()
    for key in args:
        assert key in keys, 'Returned object in correct format'
    assert len(keys) == len(args), 'Returned object in correct format'
    
# User tests
@status_is(201)
@json_body
def test_create_user(status, body):
    require_keys(body, u'revision', u'username')
    assert body[u'username'] == username, 'Username is correct'

@status_is(200)
@json_body
def test_get_user(status, body):
    require_keys(body, u'revision', u'username')
    assert body[u'username'] == username, 'Username is correct'

# Token tests    
@status_is(200)
def test_get_token(status, body):
    global token
    token = body
    
# Event tests
revision = None
id = None

@status_is(201)
@json_body
def test_create_event(status, body):
    global revision
    require_keys(body, u'revision', u'id')
    revision = body[u'revision']
    id = body[u'revision']

@status_is(200)
@json_body
def test_get_event_list(status, body):
    require_keys(body, u'events')
    assert isinstance(body[u'events'], list), 'Events list returned'
    assert len(body[u'events']) == 1, 'Events list proper size'
    assert body[u'events'][0] == revision, 'Revision number correct'
    
@status_is(200)
@json_body
def test_get_event(status, body):
    require_keys(body, u'event')
    
    require_keys(body[u'event'], u'where', u'when', u'desc', u'posted_from', u'category',
            u'creator', u'created', u'revision', u'id')
    #TODO - verify content, we probably want to set up something to make this
    #       not a pain in the ass; share the dict.  do this when the tests
    #       are cleaned up
    
@status_is(200)
def test_delete_event(status, body):
    pass

# Attendants tests
    
@status_is(200)
def test_set_attendance(status, body):
    pass
    
@status_is(200)
@json_body
def test_get_attendants_list(status, body):
    global username
    
    require_keys(body, u'attendants', u'timestamp')
    assert username in body[u'attendants'], 'User in attendants'
    assert body[u'attendants'][username] == 1, 'Status is correct'
    
def run():
    '''
    Run the automated tests
    '''
    global revision
    do = Runner(noisy=False)
    
    # Test user functionality
    do.put(test_create_user, '/users/%s/' % username, json.dumps({'password': password}))
    do.get(test_get_token, '/token/', {'username': username, 'password': password})
    do.get(test_get_user, '/users/%s/' % username, headers=auth())
    
    # Test event functionality
    event_dict = {
        u'where': u'here',
        u'when': 100,
        u'desc': u'awesomeness',
        u'posted_from': [100, 100],
    }
    do.post(test_create_event, '/events/', headers=auth(), body=json.dumps(event_dict))
    do.get(test_get_event_list, '/events/', headers=auth())
    do.get(test_get_event, '/events/%s/' % revision, headers=auth())
    do.delete(test_delete_event, '/events/%s/' % revision, headers=auth())
    
    # Test attendance functionality
    do.post(test_set_attendance, '/events/%s/attendants/' % id, headers=auth(),
            body=json.dumps({u'status': 1})) #status = attending
    do.get(test_get_attendants_list, '/events/%s/attendants/' % id, headers=auth())        
    
    