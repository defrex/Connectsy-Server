
from unittest2 import TestSuite, defaultTestLoader
import sms_user
import notification
import reply
import registration

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(sms_user))
    suite.addTests(defaultTestLoader.loadTestsFromModule(notification))
    suite.addTests(defaultTestLoader.loadTestsFromModule(reply))
    suite.addTests(defaultTestLoader.loadTestsFromModule(registration))
    return suite