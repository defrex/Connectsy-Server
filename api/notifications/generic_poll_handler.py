from tornado.web import HTTPError

import db
from utils import timestamp, require_auth
from base_handlers import BaseHandler

# Maximum number of notifications to send the client
MAX_NOTIFICATIONS = 10

class GenericPollHandler(BaseHandler):

    @require_auth
    def get(self):
        '''
        Fetch the most recent MAX_NOTIFICATIONS notifications, and clears
        the queue.
        '''
        
        # We require that the client id be sent, and that it belongs to this
        # user.  No eavesdropping allowed!
        client_id = self.get_argument(u'client_id', None)
        if not client_id or not db.objects.notification_reg.find_one({
            u'client_id': client_id, u'user': self.get_session()[u'username']}):
            raise HTTPError(403)
        
        # Our grand modification command
        modify_command = {
            # get the record for the client_id
            u'query': {u'client_id': client_id},
            # limit the query to include only MAX_NOTIFICATIONS
            u'fields': {u'notifications': {u'$slice': -MAX_NOTIFICATIONS}},
            # flush the notifications (the returned values from findandmodify
            # represent the state of the record *before* this delete is
            # performed)
            u'update': {
                # delete the notifications array member
                u'$unset': u'notifications',
            },
            # create the record if one doesn't yet exist
            u'upsert': True,
        }
        
        #execute the command
        record = db.objects.get_database().command(u'findandmodify',
            'generic_poll_client', **modify_command)
            
        #output to the client
        self.output({u'notifications': record.notifications})
            
        