#!/usr/bin/env python

import os
import sys
import functools
import httplib

# The connectsy daemon is a symlink to main.py. It fails to load the libraries
# since its current directory is init.d. This solution is a major hack.
# Feel free to improve it if inspiration strikes.
curpath = os.path.dirname(__file__)
if curpath == '/etc/init.d': curpath = '/var/www/server'

sys.path.insert(0, os.path.abspath(os.path.join(curpath, 'lib', 'tornado')))
sys.path.insert(0, os.path.abspath(os.path.join(curpath, 'lib')))


from tornado import autoreload as reload
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.web import Application
import settings


def runserver(autoreload=True):
    # Fire up command line settings
    # TODO - there's got to be a better command line module.  try optparse?
    define('port', type=int, help='Run on the given port')
    define('db_name', type=str, help='Run using this db name')
    define('runtests', type=bool, help='Run tests')
    define('testserver', type=bool, help='Run test server')
    parse_command_line()
    
    testserver = options['testserver'].value()
    del options['testserver']
    runtests = options['runtests'].value()
    del options['runtests']
    
    for setting, value in options.iteritems():
        if value.value():
            setattr(settings, setting.upper(), value.value())
    
    # httplib is not RFC 2324 compliant, so we fix that here
    httplib.responses[418] = "I'm a teapot"
    
    # Figure out how many processes to use
    processes = 1
    if not settings.DEVELOPMENT:
        processes = settings.PROCESS_COUNT if hasattr(settings, 'PROCESS_COUNT') else 0

    # late import to prevent the db from initializing
    from urls import handlers
    
    if runtests or testserver:
        setattr(settings, 'DB_NAME', settings.TEST_DB)
    
    if runtests:
        import unittest2
        from tests import main
        suite = unittest2.defaultTestLoader.loadTestsFromModule(main)
        unittest2.TextTestRunner(verbosity=2).run(suite)
    else:
        # Start Tornado
        http_server = HTTPServer(Application(handlers, 
                                             static_path=settings.static_path))
        http_server.bind(settings.PORT)
        http_server.start(processes)
        lp = IOLoop.instance()
        print 'Server running: http://0.0.0.0:%s' % settings.PORT
        if not settings.TEST and autoreload and settings.DEVELOPMENT: 
            reload.start(lp)
        lp.start()

if __name__ == "__main__":
    
    if settings.DEVELOPMENT:
        runserver()
    else:
        import daemon
        with daemon.DaemonContext():
            runserver(autoreload=False)

