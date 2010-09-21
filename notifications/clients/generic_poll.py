'''
Implementation Details:

The big issue we face is that we need atomicity on message gathering/reaping
and message creation.  This is difficult to do with standard approaches, so
instead we use mongo's findandmodify command, which runs atomically.  By
doing so, the poll message procedures are serialized per client, and we
avoid any race conditions.

To make this work, we ensure that there's a single document per client in the
`generic_poll_client` collection.  This document is of the format:

{
    client_id: ...
    notifications:
    [
        oldest
        ...
        newest
    ]
}

When a client polls for new notifications, this list will be atomically
emptied with another findandmodify command (see /api/notifications/handlers.py).
'''

import db
from notifications import notifier

class Notifier(notifier.Notifier):
    def __init__(self):
        #todo - one-time init
        pass
    
    def __del__(self):
        #todo - cleanup
        pass
        
    def send(self, user, client_id, message):
        '''
        Stores the message in the database, to be sent when the client
        asks for notifications.
        '''
        modify_command = {
            # get the record for the client_id
            u'query': {u'client_id': client_id},
            # perform the append operation
            u'update': {
                # append the message at the end of the array
                u'$push': {u'notifications': message}
            },
            # create the record if one doesn't yet exist
            u'upsert': True,
        }
        
        #execute the command
        db.objects.get_database().command(u'findandmodify',
            'generic_poll_client', **modify_command)