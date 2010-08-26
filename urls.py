from base_handlers import MainHandler
from api.events.handlers import EventHandler, EventsHandler
from api.events.invites.handlers import InvitesHandler
from api.events.attendance.handlers import AttendanceHandler
from api.events.comments.handlers import CommentsHandler
from api.tokens.handlers import TokenHandler
from api.users.handlers import UserHandler, AvatarHandler
from api.users.friends.handlers import FriendHandler, FriendsHandler

handlers = [
    (r"/", MainHandler),
    (r"/token/", TokenHandler),
    (r"/users/(?P<username>\w*)/", UserHandler),
    (r"/users/(?P<username>\w*)/avatar/", AvatarHandler),
    (r"/users/(?P<username>\w*)/friends/", FriendsHandler),
    (r"/users/(?P<username>\w*)/friends/(?P<friend>\w*)/", FriendHandler),
    (r"/events/", EventsHandler),
    (r"/events/(?P<revision>\w*)/", EventHandler),
    (r"/events/(?P<event_id>\w*)/invites/", InvitesHandler),
    (r"/events/(?P<event_id>\w*)/attendants/", AttendanceHandler),
    (r"/events/(?P<event_id>\w*)/comments/", CommentsHandler),
]

