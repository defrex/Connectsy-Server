from api.events.comments.models import Comment
from api.events.models import Event
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth
import db
import pymongo



class CommentsHandler(BaseHandler):

    def get(self, event_id):
        '''
        Gets all comments for a given event.  If the 'since' query parameter
        is provided, only comments after the specified timestamp will be 
        retrieved.
        '''
        #make sure the event exists
        if not Event.get(event_id): raise HTTPError(404)
        
        #show them comments!
        comments = Comment.find({u'event': event_id})
        comments.sort(u'timestamp', pymongo.ASCENDING)
        comments = [c.__data__ for c in comments]
        
        self.output({u'comments': comments})
    
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
        
