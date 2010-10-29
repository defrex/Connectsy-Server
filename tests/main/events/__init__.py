
from unittest2 import TestSuite, defaultTestLoader
import models
import new
import comments
import notification
import lists

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(models))
    suite.addTests(defaultTestLoader.loadTestsFromModule(new))
    suite.addTests(defaultTestLoader.loadTestsFromModule(comments))
    suite.addTests(defaultTestLoader.loadTestsFromModule(notification))
    suite.addTests(defaultTestLoader.loadTestsFromModule(lists))
    return suite