
from unittest2 import TestSuite, defaultTestLoader
import auth
import models
import following
import requests

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(auth))
    suite.addTests(defaultTestLoader.loadTestsFromModule(models))
    suite.addTests(defaultTestLoader.loadTestsFromModule(requests))
    suite.addTests(defaultTestLoader.loadTestsFromModule(following))
    return suite