from api.SMS import SMS_OUTPUT_URL
from api.SMS.models import SMSRegister
from api.SMS.sms_utils import format_date
from api.events.models import Event
from notifications import notifier
from urllib2 import HTTPError
import settings
import twilio

class Notifier(notifier.Notifier):
    
    def send(self, user, client_id, message):
        
        if message[u'type'] not in (u'invite', u'comment'):
            return False
        
        smsee = SMSRegister.get({u'event': message[u'event_id'],
                                 u'contact_number': client_id})
        if smsee is None: return False
        
        event = Event.get(message[u'event_id'])
        if event is None: return False
        
        account = twilio.Account(settings.TWILIO_ACCOUNT_SID,
                                 settings.TWILIO_AUTH_TOKEN)
        
        texts = list()
        
        if message[u'type'] == u'invite':
            texts.append('%(username)s: %(what)s' % 
                         {'username': event[u'creator'], 
                          'what': event[u'what']})
            
            t2 = ('%s just shared a plan with you on '
                  'Connectsy. ' % event[u'creator'])
            if event[u'where'] is not None:
                t2 += 'Where: %s' % event[u'where']
                if event[u'when'] is not None and event[u'when'] != 0:
                    t2 += ", "
                else:
                    t2 += ". "
            if event[u'when'] is not None:
                t2 += 'When: %s. ' % format_date(event[u'when'])
            t2 += 'Reply to comment, include #in to join.'
            texts.append(t2)
            
        elif message[u'type'] == u'comment':
            texts.append('%(commenter)s commented: %(comment)s' % message)
            if len(texts[-1]) > 160:
                texts[-1] = texts[-1][:157]+"..."
        
        try:
            for text in texts:
                account.request(SMS_OUTPUT_URL, 'POST', {
                        'To': smsee[u'contact_number'],
                        'Body': text,
                        'From': smsee[u'twilio_number'],
                    })
            return True
        except HTTPError, e:
            print e.read()
            return False
        


