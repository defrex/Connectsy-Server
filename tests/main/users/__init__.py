
from unittest2 import TestSuite, defaultTestLoader
import auth
import friending
import models

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(auth))
    suite.addTests(defaultTestLoader.loadTestsFromModule(friending))
    suite.addTests(defaultTestLoader.loadTestsFromModule(models))
    return suite