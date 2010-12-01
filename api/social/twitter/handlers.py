from api.social.twitter.models import TwitterAuth
from base_handlers import BaseHandler
from tornado.web import HTTPError
from utils import require_auth


class TwitterHandler(BaseHandler):
    
    @require_auth
    def get(self, username):
        if not username == self.get_session()[u'username']:
            raise HTTPError(403)
        
        auth = TwitterAuth.get({u'username': username})
        if auth is None:
            raise HTTPError(404)
        
        self.output({u'token': auth[u'token'], u'secret': auth[u'secret']}, 200)
    
    @require_auth
    def put(self, username):
        if not username == self.get_session()[u'username']:
            raise HTTPError(403)
        
        if TwitterAuth.get({u'username': username}) is not None:
            raise HTTPError(409)
        
        try:
            auth = {
                u'token': self.body_dict()[u'token'], 
                u'secret': self.body_dict()[u'secret'],
                u'username': username,
            }
        except KeyError, e:
            self.output({'error': 'MISSING_FIELD',
                         'field': e}, 400)
        else:
            TwitterAuth(**auth).save()
            self.set_status(201)
    
    @require_auth
    def delete(self, username):
        if not username == self.get_session()[u'username']:
            raise HTTPError(403)
        
        auth = TwitterAuth.get({u'username': username})
        if auth is None:
            raise HTTPError(404)
        
        auth.delete()
