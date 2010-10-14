
from unittest2 import TestSuite, defaultTestLoader
import server_running
import events
import auth

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(server_running))
    suite.addTests(defaultTestLoader.loadTestsFromModule(auth))
    suite.addTests(defaultTestLoader.loadTestsFromModule(events))
    return suite
