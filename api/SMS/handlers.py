
import db
from base_handlers import BaseHandler
from api.events.attendance import status

class SMSHandler(BaseHandler):
    
    def post(self):
        contact_number = self.get_argument(u'From', None)
        twilio_number = self.get_argument(u'To', None)
        body = self.get_arguemnt(u'Body', None)
        
        if None in (contact_number, twilio_number, body):
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
