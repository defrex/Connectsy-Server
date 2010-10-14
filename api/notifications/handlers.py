from base_handlers import BaseHandler
from notifications import notifiers
from notifications.models import NotificationRegister
from tornado.web import HTTPError
from utils import timestamp, require_auth
import db


class RegistrationHandler(BaseHandler):
    
    @require_auth
    def post(self):
        body = self.body_dict()
        
        #ensure all fields are supplied
        if not body or not u'client_type' in body or not u'client_id' in body:
            raise HTTPError(400)
            
        #ensure the client supported
        if not body[u'client_type'] in notifiers:
            raise HTTPError(501)
            
        NotificationRegister(**{
            u'user': self.get_session()[u'username'],
            u'timestamp': timestamp(),
            u'client_type': body[u'client_type'],
            u'client_id': body[u'client_id'],
            #the client_extra field is optional, but we want the field present
            #in the db even if the client didn't supply it
            u'client_extra': body[u'client_extra'] if u'client_extra' in body else None
        }).save()
