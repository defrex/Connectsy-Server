from api.notifications.models import GenericPollNotifications
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth
import db


class GenericPollHandler(BaseHandler):

    @require_auth
    def get(self):
        '''
        Fetch the most recent notifications, and clears the queue.
        '''
        
        # We require that the client id be sent, and that it belongs to this
        # user.  No eavesdropping allowed!
        client_id = self.get_argument(u'client_id', None)
        if not client_id or not db.objects.notification_reg.find_one({
            u'client_id': client_id, u'user': self.get_session()[u'username']}):
            raise HTTPError(403)
        
        #output to the client
        notifications = GenericPollNotifications.pop(client_id) or []
        self.output({u'notifications': notifications})
            
        
