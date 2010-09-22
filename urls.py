from api.handlers import RootHandler
from api.tokens.handlers import TokenHandler
from api.notifications.handlers import RegistrationHandler
from api.notifications.generic_poll_handler import GenericPollHandler
from api.users.handlers import UsersHandler, UserHandler, AvatarHandler
from api.users.friends.handlers import FriendHandler, FriendsHandler
from api.events.handlers import EventHandler, EventsHandler
from api.events.invites.handlers import InvitesHandler
from api.events.attendance.handlers import AttendanceHandler
from api.events.comments.handlers import CommentsHandler
from api.categories.handlers import CategoriesHandler
from api.extras.maps.handlers import MapsHandler

handlers = [
    (r"/", RootHandler),
    (r"/token/", TokenHandler),
    (r"/notifications/register/", RegistrationHandler),
    (r"/notifications/poll/", GenericPollHandler),
    (r"/users/", UsersHandler),
    (r"/users/(?P<username>\w*)/", UserHandler),
    (r"/users/(?P<username>\w*)/avatar/", AvatarHandler),
    (r"/users/(?P<username>\w*)/friends/", FriendsHandler),
    (r"/users/(?P<username>\w*)/friends/(?P<friend>\w*)/", FriendHandler),
    (r"/events/", EventsHandler),
    (r"/events/(?P<revision>\w*)/", EventHandler),
    (r"/events/(?P<event_id>\w*)/invites/", InvitesHandler),
    (r"/events/(?P<event_id>\w*)/attendants/", AttendanceHandler),
    (r"/events/(?P<event_id>\w*)/comments/", CommentsHandler),
    (r"/categories/", CategoriesHandler),
    (r"/extras/maps/", MapsHandler),
]

