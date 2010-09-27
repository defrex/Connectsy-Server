from tornado.web import HTTPError

import db
import status
import notifications
from utils import json_encoder, hash, require_auth, timestamp
from base_handlers import BaseHandler

class FriendsHandler(BaseHandler):
    
    @require_auth
    def get(self, username):
        status_type = status.ACCEPTED
        
        #allow users to get their pending friend requests
        pending = False
        if username == self.get_session()[u'username'] and self.get_argument(u'pending', False):
            status_type = status.PENDING
            pending = True
        
        list = []
        #if we're doing only pending requests, just show incoming pends
        if pending is False:
            list += [friend[u'to'] for friend in db.objects.friend.find({u'from':
                    username, u'status': status.PENDING if pending else status_type})]
        list += [friend[u'from'] for friend in db.objects.friend.find({u'to':
                username, u'status': status.PENDING if pending else status_type})]
        self.output({u'friends': list})
        
    @require_auth
    def post(self, username):
        client_user = self.get_session()[u'username']
    
        #i know you're lonely, but you still can't friend yourself
        if username == client_user:
            raise HTTPError(400)
            
        #make sure that this user actually exists
        if not db.objects.user.find_one({u'username': username}):
            raise HTTPError(404)
        
        # TODO - make sure the users aren't already friends
        
        #check for dups
        if db.objects.friend.find_one({u'to': username,
                u'from': client_user, u'status': status.PENDING}):
            raise HTTPError(409)
        
        #if a friend requests from this person to the auth'd client exists,
        #then this POST is a confirmation
        friend = db.objects.friend.find_one({u'from': username,
                u'to': client_user, u'status': status.PENDING})
        if friend:
            db.objects.friend.update({'_id': friend['_id']}, {'$set':
                    {u'status': status.ACCEPTED}})
        #otherwise, create a pending friendship
        else:
            #save the friend request in the db
            friend = {u'from': client_user, u'to': username, u'status': status.PENDING}
            db.objects.friend.save(friend)

            #send the friend notification
            notifications.send(username, {u'type': u'friend', u'username': client_user})
        
class FriendHandler(BaseHandler):
        
    @require_auth
    def delete(self, username, friend):
        user = self.get_session()[u'username']
        
        if user == username or user == friend:
            #find which person is which
            if user == username:
                other = friend
            else:
                other = username
                
            #ensure the other user actually exists
            if not db.objects.user.find_one({u'username': other}):
                return HTTPError(404)
                
            db.objects.friend.remove({u'from': username, u'to': friend})
        else:
            return HTTPError(403)

