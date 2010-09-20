import os
import uuid

from tornado.web import HTTPError

import db
from utils import json_encoder, hash, require_auth, timestamp
from base_handlers import BaseHandler
from friends import status

class UserHandler(BaseHandler):
    def put(self, username):
        #make sure we're not overwriting an existing user
        u = db.objects.user.find_one({u'username': username})
        if u is not None: 
            raise HTTPError(409)
            
        #set up the password
        password = self.body_dict().get('password')
        if not password: raise HTTPError(403)
        password = hash(password)
        
        #build the user.  make it stronger, faster...
        user = {
            u'username': username, 
            u'password': password,
            u'revision': uuid.uuid1().hex,
            u'created': int(timestamp()),
        }
        
        #save the user
        db.objects.user.insert(user)
        
        #sanitize the user manually, since it didn't come from the db
        user['_id'] = 0 #fake id so the sanitizer works
        del user['_winter'] #delete the winter revision
        user = db.sanitizers.user(user)
        
        #write the user to the response
        self.output(user, 201)
    
    @require_auth
    def get(self, username):
        u = db.objects.user.find_one({u'username': username})
        if u is None: raise HTTPError(404)
        
        #get friend status
        cur_user = self.get_session()[u'username']
        friend_status = db.objects.friend.find_one({u'from': username, 'to': cur_user})
        if friend_status:
            friend_status = friend_status[u'status']
            if friend_status == status.PENDING:
                friend_status = status.PENDING_FROM
        else:
            friend_status = db.objects.friend.find_one({u'to': username, 'from': cur_user})
            if friend_status:
                friend_status = friend_status[u'status']
                if friend_status == status.PENDING:
                    friend_status = status.PENDING_TO
                    
        #default status
        if not friend_status:
            friend_status = status.NOT_FRIEND
       
        u['friend_status'] = friend_status
        
        #write the user
        self.output(u)


avatar_dir = os.path.join(os.path.dirname(__file__),
    '..', '..', 'static', 'avatars')
class AvatarHandler(BaseHandler):
    '''
    Handles avatar serving, management.
    '''
    def find_file(self, username):
        extensions = ['png', 'jpg', 'gif']
        files = map(lambda a: os.path.join(avatar_dir, '%s.%s' % (username, a)),
            ['png', 'jpg', 'gif'])
        for extension in extensions:
            if os.path.exists(os.path.join(avatar_dir, '%s.%s' % (username, extension))):
                return '%s.%s' % (username, extension)
        return None
    
    def get(self, username):
        try:
            abspath = os.path.join(avatar_dir, self.find_file(username))
            self.redirect('/static/avatars/%s' % self.find_file(username))
        except AttributeError:
            print 'no avatar for: %s' % username
            self.redirect('/static/avatars/default.png')
    
    @require_auth
    def put(self, username):
        if not self.get_user().get(u'username') == username:
            raise HTTPError(403)
        
        #make sure we remove any old files with different extensions, because
        #they won't be overwritten
        self.delete(username)
    
        extension = None
        if 'Content-Type' in self.request.headers:
            content_type = self.request.headers['Content-Type'].split(';')[0]
            
            if content_type == 'image/png':
                extension = 'png'
            elif content_type == 'image/jpeg':
                extension = 'jpg'
            elif content_type == 'image/gif':
                extension = 'gif'
                
        if not extension:
            raise HTTPError(415)
            
        file = open(os.path.join(avatar_dir, '%s.%s' % (username, extension)), 'w')
        file.write(self.request.body)
        file.close()
        
        self.finish()
        
    @require_auth
    def delete(self, username):
        '''
        Deletes the auth'd user's avatar
        '''
        if self.get_session()[u'username'] == username:
            filename = self.find_file(username)
            if filename:
                os.remove(os.path.join(avatar_dir, filename))
        else:
            raise HTTPError(403);

