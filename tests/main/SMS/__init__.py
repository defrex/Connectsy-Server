
from unittest2 import TestSuite, defaultTestLoader
import sms_user
import notification
import reply

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(sms_user))
    suite.addTests(defaultTestLoader.loadTestsFromModule(notification))
    suite.addTests(defaultTestLoader.loadTestsFromModule(reply))
    return suite