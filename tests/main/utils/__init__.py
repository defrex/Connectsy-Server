
from unittest2 import TestSuite, defaultTestLoader
import dates
import phone_numbers

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(dates))
    suite.addTests(defaultTestLoader.loadTestsFromModule(phone_numbers))
    return suite