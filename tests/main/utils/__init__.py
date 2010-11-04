
from unittest2 import TestSuite, defaultTestLoader
import dates

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(dates))
    return suite