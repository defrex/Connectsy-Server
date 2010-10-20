#!/usr/bin/env python

import httplib
import os
import settings
import sys

# The connectsy daemon is a symlink to main.py. It fails to load the libraries
# since its current directory is init.d. This solution is a major hack.
# Feel free to improve it if inspiration strikes.
curpath = os.path.dirname(__file__)
if curpath == '/etc/init.d': curpath = '/var/www/server'

sys.path.insert(0, os.path.abspath(os.path.join(curpath, 'lib', 'tornado')))
sys.path.insert(0, os.path.abspath(os.path.join(curpath, 'lib')))

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.web import Application
from tornado import autoreload as reload

def runserver(autoreload=True):
    # Fire up command line settings
    # TODO - there's got to be a better command line module.  try optparse?
    define('port', type=int, help='Run on the given port')
    define('db_name', type=str, help='Run using this db name')
    define('runtests', type=bool, help='Run tests')
    define('testsms', type=bool, help='Include tests that send SMS messages')
    define('testserver', type=bool, help='Run test server')
    define('console', type=bool, help='Start interactive console')
    define('clean_db', type=bool, help='Delete all data')
    parse_command_line()
    
    testserver = options['testserver'].value()
    runtests = options['runtests'].value()
    console = options['console'].value()
    clean_db = options['clean_db'].value()
    
    port = options['port'].value()
    if port: settings.PORT = port
    
    if options['testsms'].value():
        settings.TEST_SMS = True
    else: 
        settings.TEST_SMS = False
    
    db_name = options['db_name'].value()
    if db_name: settings.DB_NAME = db_name
    
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
    
    if clean_db:
        import winter
        import db
        for c in winter.managers:
            db.objects.get_database().drop_collection(c)
    elif console:
        import ipdb
        ipdb.set_trace()
    elif runtests:
        import unittest2
        from tests import main
        suite = unittest2.defaultTestLoader.loadTestsFromModule(main)
        unittest2.TextTestRunner(verbosity=2).run(suite)
        autoreload = True
    else:
        # Start Tornado
        http_server = HTTPServer(Application(handlers, 
                                             static_path=settings.static_path))
        http_server.bind(settings.PORT)
        http_server.start(processes)
        lp = IOLoop.instance()
        if autoreload: 
            reload.start(lp)
        print 'Server running: http://0.0.0.0:%s' % settings.PORT
        lp.start()

if __name__ == "__main__":
    
    if settings.DEVELOPMENT:
        runserver()
    else:
        import daemon
        with daemon.DaemonContext():
            runserver(autoreload=False)

