from tornado.web import HTTPError

import db
from utils import timestamp, require_auth
from base_handlers import BaseHandler

class RegistrationHandler(object):
    
    @require_auth
    def post(self):
        body = self.body_dict()
        
        #ensure all fields are supplied
        if not body or not u'client_type' in body or not u'client_id' in body:
            raise HTTPError(400)
            
        #ensure the client supported
        if not client supported:
            raise HTTPError(501)
            
        #add the record to the db
        db.objects.notification_reg.insert({
            u'user': self.get_session()[u'username'],
            u'client_type': body[u'client_type'],
            u'client_id': body[u'client_id'],
            #the client_extra field is optional, but we want the field present
            #in the db even if the client didn't supply it
            u'client_extra': body[u'client_extra'] \
                if u'client_extra' in body else None
        })