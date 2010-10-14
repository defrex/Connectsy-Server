
from unittest2 import TestSuite, defaultTestLoader
import models
import new

def load_tests(loader, tests, pattern):
    print 'loading events tests'
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(models))
    suite.addTests(defaultTestLoader.loadTestsFromModule(new))
    return suite