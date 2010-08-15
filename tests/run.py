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

# Import the index setup file
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
import index_setup

# Import the tests
import automated
import unit
import third_party

def flush_db():
    c = pymongo.connection.Connection()
    
    #drop the entire database
    c.drop_database(settings.TEST_DB)
    
    #rebuild the indexes, otherwise and GEO2D stuff will be screwed
    for collection in index_setup.indexes:
        #build a list so we can ensure the indexes in one call
        l = []
        for field, direction in index_setup.indexes[collection].iteritems():
            l.append((field, direction))
        #ensure that the indexes exist
        c[settings.TEST_DB][collection].ensure_index(l)
        
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
    
