import uuid

import pymongo
from tornado.web import HTTPError

import db
from api.events.attendance import status
from utils import timestamp, require_auth
from base_handlers import BaseHandler

class CommentsHandler(BaseHandler):

    def get(self, event_id):
        '''
        Gets all comments for a given event.  If the 'since' query parameter
        is provided, only comments after the specified timestamp will be 
        retrieved.
        '''
        #make sure the event exists
        if not db.objects.event.find_one(event_id):
            raise HTTPError(404)
        
        #grab the optional offset
        since = self.get_argument(u'since', None) #TODO - sanitize?
        
        #prep the query
        query = {
            u'event': event_id,
        }
        if since:
            query[u'timestamp'] = {'$gt': since}
        
        #show them comments!
        comments = db.objects.comment.find(query).sort(u'timestamp', pymongo.ASCENDING)
        self.output({u'comments': [c for c in comments]})
    
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
        if not u'nonce' in body:
            body[u'nonce'] = uuid.uuid1()
        else:
            #if another comment exists with this nonce, it's a double-post
            if db.objects.comment.find_one({u'nonce': body[u'nonce'], \
            u'event': event_id, u'user': self.get_session()[u'username']}):
                raise HTTPError(409)
            
        #create the comment
        comment = {
            u'nonce': body[u'nonce'],
            u'comment': body[u'comment'],
            u'timestamp': timestamp(),
            u'event': event_id,
            u'user': self.get_session()[u'username']
        }
        db.objects.comment.insert(comment)
        
        # Success!
        
