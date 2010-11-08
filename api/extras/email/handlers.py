
from base_handlers import BaseHandler
from tornado.web import HTTPError

class BetaEmailHandler(BaseHandler):
    
    def get(self):
        #grab the sorting type from the args
        email = self.get_argument('email', None)
        if email is None: raise HTTPError(403)
        
        with open('/var/log/beta_emails.txt', 'a') as f:
            f.write('%s\n' % email)
        
        #self.redirect('http://connectsy.com/')