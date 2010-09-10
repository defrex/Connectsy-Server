
from pymongo import DESCENDING

from base_handlers import BaseHandler
import db

class MapsHandler(BaseHandler):
    
    def get(self):
        #grab the sorting type from the args
        sort = self.get_argument('sort', None)
        
        #grab lat/lng from the query, defaulting to toronto
        lat = float(self.get_argument('lat', '43.652527'))
        lng = float(self.get_argument('lng', '-79.381961'))
        events = db.objects.event.find({u'posted_from': {u'$near': [lat, lng]}})
        events = events.sort(u'when', direction=DESCENDING)
        resp = list()
        for e in events:
            resp.append({
                    u'rev': e[u'revision'],
                    u'loc': e[u'posted_from'],
                })
        self.output(resp)