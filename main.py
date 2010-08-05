#!/usr/bin/python

import sys
import os
import httplib

# The connectsy daemon is a symlink to main.py. It fails to load the libraries
# since its current directory is init.d. This solution is a major hack.
# Feel free to improve it if inspiration strikes.
curpath = os.path.dirname(__file__)
if curpath == '/etc/init.d': curpath = '/var/www/server'

sys.path.insert(0, os.path.abspath(os.path.join(curpath, 'lib', 'tornado')))
sys.path.insert(0, os.path.abspath(os.path.join(curpath, 'lib')))

from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado import autoreload as reload
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from daemon import Daemon

import settings

def runserver(autoreload=True):
    # Fire up command line settings
    # TODO - there's got to be a better command line module.  try optparse?
    define('port', type=int, help='Run on the given port')
    define('db_name', type=str, help='Run using this db name')
    parse_command_line()
    for setting, value in options.iteritems():
        if value.value():
            setattr(settings, setting.upper(), value.value())
    
    # httplib is not RFC 2324 compliant, so we fix that here
    httplib.responses[418] = "I'm a teapot"
    
    # Start Tornado
    from urls import handlers # late import to prevent the db from initializing
    http_server = HTTPServer(Application(handlers))
    http_server.listen(settings.PORT)
    lp = IOLoop.instance()
    if autoreload: 
        reload.start(lp)
    print 'Server running: http://127.0.0.1:%s' % settings.PORT
    lp.start()

class ConsyDaemon(Daemon):
    def run(self):
        runserver(autoreload=False)

if __name__ == "__main__":
    
    if settings.DEVELOPMENT:
        runserver()
    else:
        import logging
        LOG_FILENAME = '/var/log/api.dev.connectsy.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
        d = ConsyDaemon('/var/run/consy.pid')
        if 'start' == sys.argv[1]:
            print 'starting'
            d.start()
            print 'Connectsy daemon started'
        elif 'stop' == sys.argv[1]:
            print 'stopping'
            d.stop()
            print 'Connectsy daemon stopped'
        elif 'restart' == sys.argv[1]:
            print 'restarting'
            d.restart()
            print 'Connectsy daemon restarted'
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)

