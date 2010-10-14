#!/usr/bin/env python

'''
Connectsy test runner.
'''
import unittest2
import sys
import os

import main

def start_test_server():
    pass
    
def stop_test_server():
    pass

def run():
    print ''
    print '---------------------------'
    print 'Running tests'
    print '---------------------------'
    suite = unittest2.defaultTestLoader.loadTestsFromModule(main)
    unittest2.TextTestRunner(verbosity=2).run(suite)

