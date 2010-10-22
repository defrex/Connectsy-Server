
from unittest2 import TestSuite, defaultTestLoader

import models

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(models))
    return suite