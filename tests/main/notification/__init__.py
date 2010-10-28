
from unittest2 import TestSuite, defaultTestLoader
import generic_poll

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(generic_poll))
    return suite