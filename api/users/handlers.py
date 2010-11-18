
from PIL import Image #@UnresolvedImport
from StringIO import StringIO
from api.users.followers.models import Follower
from api.users.models import User
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth, timestamp
import os
import re
import uuid



username_sanitizer = re.compile(r"\W")

class UsersHandler(BaseHandler):

    @require_auth
    def get(self):
        #grab and sanitize the query
        q = self.get_argument(u'q', u'')
        q = username_sanitizer.sub('', q)
        #query: *q*
        users = User.find({u'username': re.compile(q)})
        self.output([user[u'username'] for user in users])


class UserHandler(BaseHandler):
    def put(self, username):
        username = username.lower()
        #make sure we're not overwriting an existing user
        u = User.get({u'username': username})
        if u is not None: 
            raise HTTPError(409)
        
        #set up the password
        password = self.body_dict().get('password')
        if not password: raise HTTPError(403)
        
        User(**{
            u'username': username, 
            u'password': User.hash_password(password),
            u'number': self.body_dict().get('number'),
            u'revision': uuid.uuid1().hex,
            u'created': int(timestamp()),
        }).save()
        
        self.set_status(201)
    
    @require_auth
    def get(self, username):
        u = User.get({u'username': username})
        if u is None: raise HTTPError(404)
        
        cur_user = self.get_session()[u'username']
        
        follower = Follower.get({u'follower': username, u'followee': cur_user})
        following = Follower.get({u'follower': cur_user, u'followee': username})
        
        self.output({
            u'username': u['username'],
            u'created': u[u'created'],
            u'id': u[u'id'],
            u'follower': (follower is not None),
            u'following': (following is not None),
        })


avatar_dir = os.path.join(os.path.dirname(__file__),
    '..', '..', 'static', 'avatars')
class AvatarHandler(BaseHandler):
    '''
    Handles avatar serving, management.
    '''
    def find_file(self, username):
        extensions = ['png', 'jpg', 'gif']
        for extension in extensions:
            if os.path.exists(os.path.join(avatar_dir, '%s.%s' % (username, extension))):
                return '%s.%s' % (username, extension)
        return None
    
    def get(self, username):
        file = self.find_file(username)
        if file is None: raise HTTPError(404)
        self.redirect('/static/avatars/%s' % self.find_file(username))
    
    @require_auth
    def put(self, username):
        if not self.get_session()[u'username'] == username:
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
        
        file = StringIO(self.request.body)
        image = Image.open(file)
        image.thumbnail((100, 100), Image.ANTIALIAS)
        image.save(os.path.join(avatar_dir, '%s.png' % (username)))
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

