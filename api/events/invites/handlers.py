
import json

from tornado.web import HTTPError

import db
import notifications
from api.events.attendance import status
from utils import timestamp, require_auth, json_encoder
from base_handlers import BaseHandler
from api.users.friends import status as friend_status
from api import SMS

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
        
        if u'users' in body:
            users = body[u'users']
            
            #friends is a special case
            if users == u'friends':
                #get friends
                username = self.get_session()[u'username']
                friends = []
                friends += [friend[u'to'] for friend in db.objects.friend.find({u'from':
                        username, u'status': friend_status.ACCEPTED})]
                friends += [friend[u'from'] for friend in db.objects.friend.find({u'to':
                        username, u'status': friend_status.ACCEPTED})]
                users = friends 
           
            #grab the existing attendance info
            attendance = db.objects.attendance.find({u'event': event_id})
            #only create new attendances for people who weren't already there
            for att in attendance:
                #man, hash tables sure are lovely for avoiding O(n^2) runtimes...
                if att[u'username'] in users:
                    del users[att[u'username']]
                    
            #prevent people from inviting themselves
            if event[u'creator'] in users:
                del users[event[u'creator']]
                
            for username in users:
                #send the invite notification
                notifications.send(username, {u'type': 'invite', u'event_revision': event[u'revision']})
                #build out the new attendance object
                db.objects.attendance.insert({u'username': username,
                        u'event': event_id, u'timestamp': timestamp(),
                        u'status': status.INVITED})
        
        if u'contacts' in body:
            if u'users' in body and body[u'users'] != u'friends':
                for contact in body[u'contacts']:
                    u = db.objects.user.find_one({u'number': contact[u'number']})
                    if u is not None:
                        body[u'users'] = body.get(u'users') or list()
                        if not u.username in body[u'users']:
                            body[u'users'].append(u.username)
                        del body[u'contacts'][contact]
            try:
                SMS.register(event, body[u'contacts'])
            except SMS.OutOfNumbersException, e:
                self.write(json.dumps({'error': 'OUT_OF_NUMBERS',
                                       'contacts': e.contacts,
                                       'event_revision': event[u'revision']}))
                self.set_status(409)
            SMS.new_event(event, u'new')
        
