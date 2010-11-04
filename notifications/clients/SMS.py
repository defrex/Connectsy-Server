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
        
        if message[u'type'] == u'invite':
            message = ('%(username)s invited you to %(where)s %(when)s. '
                       'Reply to comment, include #in to join, #what or '
                       '#who for more info. -Connectsy') % {
                            'username': event[u'creator'],
                            'where': event[u'where'],
                            'when': format_date(event[u'when']),
                        }
            import ipdb; ipdb.set_trace()
        elif message[u'type'] == u'comment':
            message = '%(commenter)s commented: %(comment)s' % message
            if len(message) > 160:
                message = message[:157]+"..."
        
        try:
            account.request(SMS_OUTPUT_URL, 'POST', {
                    'To': smsee[u'contact_number'],
                    'Body': message,
                    'From': smsee[u'twilio_number'],
                })
            return True
        except HTTPError, e:
            print e.read()
            return False
        


