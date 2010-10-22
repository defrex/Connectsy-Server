from api.events.comments.models import Comment
from api.events.models import Event
from api.users.models import User
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth
import db
import pymongo



class CommentsHandler(BaseHandler):

    def get(self, event_id):
        '''
        Gets all comments for a given event.
        '''
        #make sure the event exists
        if not Event.get(event_id): raise HTTPError(404)
        
        #show them comments!
        comments = Comment.find({u'event': event_id})
        comments.sort(u'timestamp', pymongo.ASCENDING)
        
        ret_coms = []
        for c in comments:
            user = User.get(c[u'user'])
            ret = c.__data__
            ret[u'username'] = user.__data__.get(u'username', None)
            if ret[u'username'] is None:
                del ret[u'username']
            ret[u'display_name'] = user.__data__.get(u'display_name', None)
            if ret[u'display_name'] is None:
                del ret[u'display_name']
            ret_coms.append(ret)
        
        self.output({u'comments': ret_coms})
    
    @require_auth
    def post(self, event_id):
        #make sure the event exists
        if not db.objects.event.find_one(event_id):
            raise HTTPError(404)
    
        #grab the data
        body = self.body_dict()
        #comment body is required, and must have content
        if not u'comment' in body:
            raise HTTPError(400)
            
        #nonce is optional
        if u'nonce' in body:
            #if another comment exists with this nonce, it's a double-post
            if Comment.get({u'nonce': body[u'nonce'],
                            u'event': event_id, 
                            u'user': self.get_session()[u'username']}):
                raise HTTPError(409)
        
        #create the comment
        Comment(**{
            u'comment': body[u'comment'],
            u'event': event_id,
            u'username': self.get_session()[u'username']
        }).save()
        
        # Success!
        
