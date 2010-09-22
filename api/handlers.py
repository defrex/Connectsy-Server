import time

import settings
from base_handlers import BaseHandler

start_time = time.time()
class RootHandler(BaseHandler):
    def get(self):
        version = u'0.2'
        mode = u'Development' if settings.DEVELOPMENT else u'Production'
        uptime = time.time() - start_time
        
        self.set_status(418)
        self.set_header('X-Server', 'Connectsy-Teapot/0.1 Freshly Brewed')
        self.set_header('Content-Type', 'text/plain; charset=UTF-8')
        self.write(u'''
        Connectsy API Server
            Version: %s
            Mode:    %s
            Uptime:  %s seconds
            
        "Everything should be made as simple as possible, but not simpler."
          -- Albert Einstein
        ''' % (version, mode, uptime))
        self.finish()
