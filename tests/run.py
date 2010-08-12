#!/usr/bin/python

'''
Connectsy test runner.
'''
import os
import sys
import subprocess

import settings

# Import PyMongo
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
import pymongo

# Import the tests
import automated
import unit
import third_party

def flush_db():
    c = pymongo.connection.Connection()
    c.drop_database(settings.TEST_DB)
    c.disconnect()
    
def start_test_server():
    pass
    
def stop_test_server():
    pass

if __name__ == '__main__':
    print ''
    print '---------------------------'
    print 'Running automated tests'
    print '---------------------------'
    flush_db()
    automated.run()
    
    print ''
    print '---------------------------'
    print 'Running unit tests'
    print '---------------------------'
    flush_db()
    unit.run()
    
    print ''
    print '---------------------------'
    print 'Running third-party tests'
    print '---------------------------'
    flush_db()
    third_party.run()
    
    print ''
    flush_db() # boy scout
    
