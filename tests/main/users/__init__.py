
from unittest2 import TestSuite, defaultTestLoader
import auth
import friending

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(auth))
    suite.addTests(defaultTestLoader.loadTestsFromModule(friending))
    return suite