
from unittest2 import TestSuite, defaultTestLoader
import auth
import models
import following
import requests
import search

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(auth))
    suite.addTests(defaultTestLoader.loadTestsFromModule(models))
    suite.addTests(defaultTestLoader.loadTestsFromModule(requests))
    suite.addTests(defaultTestLoader.loadTestsFromModule(following))
    suite.addTests(defaultTestLoader.loadTestsFromModule(search))
    return suite