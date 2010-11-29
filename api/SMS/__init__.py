
from api.SMS.models import SMSRegister
from api.SMS.sms_utils import format_date, normalize_phone_number
from datetime import datetime
from notifications.models import NotificationRegister
from urllib2 import HTTPError
from utils import timestamp, from_timestamp
import db
import pytz
import settings
import twilio


class OutOfNumbersException(Exception):
    def __init__(self, contacts, users):
        self.out_of_numbers = contacts
        self.registered = users
    
    def __str__(self):
        return 'There are no numbers left for: '+self.out_of_numbers


def register(event, contacts, tz=None):
    #late import to User model can use phone number normalizer
    from api.users.models import User
    if not u'id' in event:
        event[u'id'] = str(event[u'_id'])
    
    registered = list()
    out_of_numbers = list()
    has_username = list()
    
    for contact in contacts:
        contact[u'number'] = contact[u'number']
        user = User.get({u'number': contact[u'number']})
        if user is None:
            user = User(number=contact[u'number'], 
                        display_name=contact[u'name'])
            user.save()
        
        # Connectsy users don't get SMS
        if user[u'username'] is not None:
            has_username.append(user)
            continue
        
        # make sure this user still has numbers available
        potential_numbers = [n for n in settings.TWILIO_NUMBERS]
        for reg in SMSRegister.find({u'contact_number': contact[u'number']}):
            if from_timestamp(reg[u'expires']) > datetime.now(pytz.utc):
                potential_numbers = [n for n in potential_numbers 
                                     if n != reg[u'twilio_number']]
        if len(potential_numbers) == 0:
            out_of_numbers.append(contact)
            continue
        
        if tz: tz = tz.zone
        else: tz = 'America/Toronto'
        
        registered.append(user)
        r = SMSRegister(contact_number=contact[u'number'], 
                    twilio_number=potential_numbers[0], 
                    event=event[u'id'], 
                    expires=event[u'when'],
                    user=user[u'id'],
                    tz=tz)
        r.save()
        
        #register with the notifications system as well
        note = {
            u'user': user[u'id'],
            u'timestamp': timestamp(),
            u'client_type': 'SMS',
            u'client_id': r[u'contact_number'],
        }
        NotificationRegister(**note).save()
    
    return registered, out_of_numbers, has_username



