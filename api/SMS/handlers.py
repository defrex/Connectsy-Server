
from api.SMS import SMS_OUTPUT_URL
from api.SMS.models import SMSRegister
from api.events.attendance import status
from api.events.attendance.models import Attendant
from api.events.comments.models import Comment
from api.events.models import Event
from api.users.models import User
from base_handlers import BaseHandler
from tornado.web import HTTPError
import db
import settings
import twilio
import urllib2



class SMSHandler(BaseHandler):
    
    def post(self):
        try:
            contact_number = self.request.arguments[u'From'][0]
            twilio_number = self.request.arguments[u'To'][0]
            body = self.request.arguments[u'Body'][0]
        except KeyError, e:
            print e
            raise HTTPError(400)
        print contact_number, twilio_number, body
        sms_reg = SMSRegister.get({u'contact_number': contact_number,
                                   u'twilio_number': twilio_number})
        if sms_reg is None: raise HTTPError(404)
        
        event = Event.get(sms_reg[u'event'])
        if event is None: raise HTTPError(404)
        
        user = User.get(sms_reg[u'user'])
        if user is None: raise HTTPError(404)
        
        account = twilio.Account(settings.TWILIO_ACCOUNT_SID,
                                 settings.TWILIO_AUTH_TOKEN)
        
        if '#who' in body:
            message = 'Who\'s invited: '
            
            adding = list()
            plus = 0
            for att in db.objects.attendance.find({u'event': sms_reg[u'event']}):
                if att[u'status'] == status.ATTENDING:
                    if len(adding) < 9:
                        adding.append(att[u'username'])
                    else:
                        plus += 1
            for u in adding:
                message += u+', '
            if plus > 0:
                message += 'and '+plus+' others.'
            else:
                message = message[:-2]
            try:
                account.request(SMS_OUTPUT_URL, 'POST', {
                    'To': contact_number,
                    'From': twilio_number,
                    'Body': message,
                })
            except urllib2.HTTPError, e:
                raise
        
        if '#what' in body:
            message = 'What: '+event[u'what']+' -Get the app'
            
            account.request(SMS_OUTPUT_URL, 'POST', {
                    'To': contact_number,
                    'From': twilio_number,
                    'Body': message,
                })
        
        if '#in' in body:
            att = Attendant.get({u'user': user[u'id'], u'event': event[u'id']})
            if att is None: raise HTTPError(404)
            
            att[u'status'] = status.ATTENDING
            att.save(safe=True)
        
        if len(body .replace('#in', '')
                    .replace('#who', '')
                    .replace('#what', '')):
            Comment(**{
                u'comment': body,
                u'event': event[u'id'],
                u'user': user[u'id']
            }).save()
        
        
         


