
from api import SMS
from api.events.attendance.models import Attendant
from api.users.friends import status as friend_status
from api.users.models import User
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth
import db
import json
import notifications



class InvitesHandler(BaseHandler):
    '''
    Manages invites
    '''
    
    @require_auth
    def post(self, event_id):
        #grab the event from the db
        event = db.objects.event.find_one(event_id)
        
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
            users = body.get(u'users', list())
            
            #friends is a special case
            if users == u'friends':
                #get friends
                username = self.get_session()[u'username']
                friends = []
                friends += [friend[u'to'] for friend in db.objects.friend.find(
                        {u'from': username, u'status': friend_status.ACCEPTED})]
                friends += [friend[u'from'] for friend in db.objects.friend.find(
                        {u'to': username, u'status': friend_status.ACCEPTED})]
                users = friends 
            
            #prevent people from inviting themselves
            if event[u'creator'] in users:
                del users[event[u'creator']]
            
            # convert usernames to user objects
            users = list(User.find({u'username': {'$in': users}}))
            
            if u'contacts' in body:
                registered, out_of_numbers, has_username = SMS.register(event, 
                                                            body[u'contacts'])
                users += has_username
                users += registered
                if len(out_of_numbers) > 0:
                    self.write(json.dumps({'error': 'OUT_OF_NUMBERS',
                                           'contacts': out_of_numbers,
                                           'event_revision': event[u'revision']}))
                    self.set_status(409)
            
            for user in users:
                Attendant(user=user[u'id'], event=event_id).save()
                #send the invite notification
                if user[u'username'] is not None: name = user[u'username']
                else: name = user[u'id']
                
                notifications.send(name, {u'type': 'invite', 
                                          u'event_revision': event[u'revision'],
                                          u'event_id': event[u'id']})
        






