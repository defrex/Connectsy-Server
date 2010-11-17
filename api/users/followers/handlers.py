from api.users.followers.models import Follower
from base_handlers import BaseHandler
from tornado.httpclient import HTTPError
import notifications


class FollowerHandler(BaseHandler):
    
    def get(self, username):
        followers = Follower.find({u'followee': username}).followers(users=False)
        self.output(followers, 200)
    
    def post(self, username):
        follow = self.body_dict().get(u'follow')
        if follow is None: raise HTTPError(403)
        
        follower = Follower.get({u'follower': self.get_user()[u'username'],
                                 u'followee': username})
        
        if follow and follower is None:
            Follower(**{u'follower': self.get_user()[u'username'],
                        u'followee': username}).save()
            notifications.send(username, {u'type': u'follow', 
                                          u'username': self.get_user()[u'username']})
        elif not follow and follower is not None:
            follower.delete()


class FollowingHandler(BaseHandler):
    
    def get(self, username):
        followees = Follower.find({u'follower': username}).followees(users=False)
        self.output(followees, 200)
