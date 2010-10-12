
from datetime import datetime

from urllib2 import HTTPError
from lib import twilio

import settings
import db
from utils import timestamp, from_timestamp

from api.SMS.sms_utils import format_date

SMS_INPUT_URL = u'http://%s/extras/SMS/' % settings.DOMAIN
SMS_OUTPUT_URL = u'/%(api_version)s/Accounts/%(account_sid)s/SMS/Messages' % {
    u'api_version': u'2010-04-01',
    u'account_sid': settings.TWILIO_ACCOUNT_SID,
}


class OutOfNumbersException(Exception):
     def __init__(self, contacts):
         self.contacts = contacts
     def __str__(self):
         return 'There are no numbers left for: '+contacts


def register(event, contacts):
    out_of_numbers = list()
    if not u'id' in event:
        event[u'id'] = str(event[u'_id'])
    
    for contact in contacts:
        registered = db.objects.sms_reg.find({u'contact_number': contact[u'number']})
        potential_numbers = [n for n in settings.TWILIO_NUMBERS]
        for reg in registered:
            if from_timestamp(reg[u'expires']) > datetime.now():
                potential_numbers = [n for n in potential_numbers if n != reg[u'twilio_number']]
        if len(potential_numbers) == 0:
            out_of_numbers.append(contact)
        else:
            db.objects.sms_reg.update({u'contact_number': contact[u'number'],
                                       u'twilio_number': potential_numbers[0]},
                                      {u'contact_number': contact[u'number'],
                                       u'twilio_number': potential_numbers[0],
                                       u'name': contact[u'name'],
                                       u'event': event[u'id'],
                                       u'expires': event[u'when']},
                                      upsert=True)
    if len(out_of_numbers) > 0:
        raise OutOfNumbersException(out_of_numbers)


def new_event(event, what):
    smsees = db.objects.sms_reg.find({u'event': event[u'id']})
    if smsees.count() == 0: return
    account = twilio.Account(settings.TWILIO_ACCOUNT_SID,
                             settings.TWILIO_AUTH_TOKEN)
    message = ('%(username)s invited you to %(where)s %(when)s. '
               'Reply to comment, include #in to join, #what or '
               '#who for more info. -Connectsy') % {
                    'username': event[u'creator'],
                    'where': event[u'where'],
                    'when': format_date(event[u'when']),
                }
    for smsee in smsees:
        try:
            account.request(SMS_OUTPUT_URL, 'POST', {
                    'To': smsee[u'contact_number'],
                    'From': smsee[u'twilio_number'],
                    'Body': message,
                })
            print 'success'
        except HTTPError, e:
            print e.read()
            raise


