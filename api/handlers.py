import time

import settings
from base_handlers import BaseHandler

def nice_time(span):
    '''
    Generates a nice time description from a span
    '''
    if span > 60 * 60 * 24: #days
        return u'%s days' % (span / (60 * 60 * 24))
    elif span > 60 * 60: #hours
        return u'%s hours' % (span / 360)
    elif span > 60: #minutes
        return u'%s minutes' % (span / 60)
    else:
        return u'%s seconds' % span
        

start_time = time.time()
class RootHandler(BaseHandler):
    def get(self):
        version = u'1.0'
        mode = u'Development' if settings.DEVELOPMENT else u'Production'
        uptime = time.time() - start_time
        
        self.set_status(200) # As fun as 418 was, pingdom don't like it :(
        self.set_header('Content-Type', 'text/plain; charset=utf-8')
        self.write(u'''
        Connectsy API Server
            Version: %s
            Mode:    %s
            Uptime:  %s
            
        "Everything should be made as simple as possible, but not simpler."
          -- Albert Einstein
        ''' % (version, mode, nice_time(uptime)))
        self.finish()
