
from unittest2 import TestSuite, defaultTestLoader
import twitter

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(twitter))
    return suite
