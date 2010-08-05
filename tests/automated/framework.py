'''
A small REST testing framework.  Ruby has inspired me: tests should be
beautiful, and xUnit is retarded.

Obviously, this seriously lacks documentation.  Check out the test suite
for usage.
'''

import httplib
import urllib
import traceback
from sys import stderr, stdout

import settings
from utils import json

def status_is(required_code):
    '''
    Fails the test unless the returned status code matches the one supplied.
    '''
    def dec(f):
        def func(code, body):
            if code != required_code:
                raise CustomException('Status code was %s, expected %s'
                    % (code, required_code))
            return f(code, body)
        #retain the decorated function's original name
        func.func_name = f.func_name
        return func
    return dec

def json_body(f):
    '''
    Passes a dictionary to the test function, parsed from JSON.  If the JSON
    is malformed the test will fail automatically.
    '''
    def func(code, body):
        try:
            body = json.loads(body)
        except:
            raise CustomException('JSON not well formed')
            
        return f(code, body)
    #retain the decorated function's original name
    func.func_name = f.func_name
    return func

class Runner(object):
    '''
    Test runner class
    '''
    def __init__(self, noisy=False):
        self.connection = httplib.HTTPConnection(settings.TEST_SERVER) 
        self.noisy = noisy
        
    def __del__(self):
        self.connection.close()
        
    def _get_result(self, callback, response):
        try:
            callback(response.status, response.read())
            if self.noisy:
                stdout.write('Passed %s\n' % callback.func_name)
        except CustomException, e:
            stderr.write('Failed %s: %s\n' % (callback.func_name, e.args[0]))
        except AssertionError, e:
            stderr.write('Failed %s on: %s\n' % (callback.func_name, e.args[0]))
        except:
            stderr.write('Failed %s with exception:\n' % (callback.func_name))
            traceback.print_exc(file=stderr)
            
    # Testing methods.  Use these!
        
    def get(self, callback, url, args={}, headers={}):
        #append the args to the url
        if len(args):
            url += '?'
            for arg, value in args.iteritems():
                url += '%s=%s&' % tuple(map(urllib.quote, [arg, value]))
                
        self.connection.request('GET', url, headers=headers)
        response = self.connection.getresponse()
        self._get_result(callback, response)
    
    def post(self, callback, url, body=u'', headers={}):
        self.connection.request('POST', url, body=body, headers=headers)
        response = self.connection.getresponse()
        self._get_result(callback, response)
        
    def put(self, callback, url, body=u'', headers={}):
        self.connection.request('PUT', url, body=body, headers=headers)
        response = self.connection.getresponse()
        self._get_result(callback, response)
        
    def delete(self, callback, url, headers={}):
        self.connection.request('DELETE', url, headers=headers)
        response = self.connection.getresponse()
        self._get_result(callback, response)
        
class CustomException(BaseException):
    '''
    Used by decorators to generate better error messages
    '''
    pass