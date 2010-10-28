
from unittest2 import TestSuite, defaultTestLoader
import server_running
import events
import users
import SMS
import db
import notification

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    suite.addTests(defaultTestLoader.loadTestsFromModule(server_running))
    suite.addTests(defaultTestLoader.loadTestsFromModule(db))
    suite.addTests(defaultTestLoader.loadTestsFromModule(notification))
    suite.addTests(defaultTestLoader.loadTestsFromModule(users))
    suite.addTests(defaultTestLoader.loadTestsFromModule(events))
    suite.addTests(defaultTestLoader.loadTestsFromModule(SMS))
    return suite
