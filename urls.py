from base_handlers import MainHandler
from api.events.handlers import EventHandler, EventsHandler
from api.events.attendance.handlers import AttendanceHandler
from api.tokens.handlers import TokenHandler
from api.users.handlers  import UserHandler, AvatarHandler

handlers = [
    (r"/", MainHandler),
    (r"/token/", TokenHandler),
    (r"/users/(?P<username>\w*)/", UserHandler),
    (r"/users/(?P<username>\w*)/avatar/", AvatarHandler),
    (r"/events/", EventsHandler),
    (r"/events/(?P<revision>\w*)/", EventHandler),
    (r"/events/(?P<event_id>\w*)/attendants/", AttendanceHandler),
]

