
from datetime import datetime, timedelta
import pytz
from utils import from_timestamp
import re


def format_date(raw_date, tz='Etc/UTC'):
    print 'formatting date to tz', tz
    raw_date = int(raw_date)
    tz = pytz.timezone(tz)
    
    date = from_timestamp(raw_date).astimezone(tz)
    today = datetime.now(pytz.utc).astimezone(tz)
    
    delta = date - today
    
    if date.year == today.year:
        if delta < timedelta(days=7):
            if (date.day - today.day) < 2:
                if (date.day - today.day) == 0:
                    format = 'Today'
                else:
                    format = 'Tomorrow'
            else:
                format = '%A'
        else:
            format = '%b. %d'
    else:
        format = '%b. %d, %Y'
    
    formatted_date = date.strftime(format)
    formatted_time = date.strftime('%I:%M%p')
    return '%s at %s' % (formatted_date, formatted_time.lstrip('0'))

def normalize_phone_number(number):
    number = re.sub('[^\d]', '', number)
    if len(number) == 10:
        number = '1%s' % number
    return number

