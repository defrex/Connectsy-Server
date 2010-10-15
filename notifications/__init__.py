from clients import notifiers
from notifications.models import NotificationRegister
import db


def send(user, message):
    '''
    Sends a message to all of a user's registered listeners
    '''
    listeners = NotificationRegister.find({u'user': user})
    
    results = list()
    for listener in listeners:
        results.append(notifiers[listener[u'client_type']]
                       .send(user, listener[u'client_id'], message))
    #this return is mainly to make all this testable
    return results
    