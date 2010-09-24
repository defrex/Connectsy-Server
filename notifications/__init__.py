from clients import notifiers

import db

def send(user, message):
    '''
    Sends a message to all of a user's registered listeners
    '''
    listeners = db.objects.notification.find_all({u'user': user})
    for listener in listeners:
        notifiers[listener[u'client_type']].send(user, listener[u'client_id'],
                message)
    