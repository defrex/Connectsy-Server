
from tornado.web import HTTPError
from lib import twilio

import db
from base_handlers import BaseHandler
from api.events.attendance import status
import settings

class SMSHandler(BaseHandler):
    
    def post(self):
        try:
            contact_number = self.request.arguments[u'From'][0]
            twilio_number = self.request.arguments[u'To'][0]
            body = self.request.arguments[u'Body'][0]
        except KeyError:
            raise HTTPError(400)
        
        sms_reg = db.objects.sms_reg.find_one({u'contact_number': contact_number,
                                               u'twilio_number': twilio_number})
        if sms_reg is None:
            raise HTTPError(404)
        
        event = db.objects.event.find_one(sms_reg[u'event'])
        
        account = twilio.Account(settings.TWILIO_ACCOUNT_SID,
                                 settings.TWILIO_AUTH_TOKEN)
        
        if '#who' in body:
            message = 'Who: '
            
            adding = list()
            plus = 0
            for att in db.objects.attendance.find({u'event': sms_reg[u'event']}):
                if att[u'status'] == status.ATTENDING:
                    if len(adding) < 10:
                        adding.append(attt[u'username'])
                    else:
                        plus += 1
            for u in adding:
                message += u+', '
            if plus > 0:
                message += 'and '+plus+' others.'
            
            account.request(SMS_OUTPUT_URL, 'POST', {
                    'To': contact_number,
                    'From': twilio_number,
                    'Body': message,
                })
        
        if '#what' in body:
            message = 'What: '+event[u'what']+' -Get the app'
