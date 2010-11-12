
from api.events.models import Event
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth
import json



class InvitesHandler(BaseHandler):
    '''
    Manages invites
    '''
    
    @require_auth
    def post(self, event_id):
        #grab the event from the db
        event = Event.get(event_id)
        
        #make sure the event exists
        if event is None:
            raise HTTPError(404)

        #make sure the client is the event's owner
        if not event[u'creator'] == self.get_session()[u'username']:
            raise HTTPError(403)
            
        #make sure the request has the correct info in the body
        body = self.body_dict()
        if not body or (not u'users' in body and not u'contacts' in body):
            raise HTTPError(400)
        
        if u'users' in body or u'contacts' in body:
            users = body.get(u'users')
            #friends is a special case
            if users == u'friends':
                users = self.get_user().friends()
            
            out_of_numbers = event.invite(usernames=users, 
                                          contacts=body.get(u'contacts'))
            if out_of_numbers is not None:
                self.write(json.dumps({'error': 'OUT_OF_NUMBERS',
                                       'contacts': out_of_numbers,
                                       'event_revision': event[u'revision']}))
                self.set_status(409)
        






