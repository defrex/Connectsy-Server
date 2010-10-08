
from datetime import datetime, timedelta

from utils import from_timestamp

def format_date(raw_date):
    date = from_timestamp(raw_date)
    today = datetime.now()
    delta = date - today
    if date.year == today.year:
        if delta < timedelta(days=7):
            if (date.day - today.day) < 2:
                if (date.day - today.day) == 0:
                    format = 'Today at %I:%M%p'
                else:
                    format = 'Tomorrow at %I:%M%p'
            else:
                format = '%A at %I:%M%p'
        else:
            format = '%b. %d at %I:%M%p'
    else:
        format = '%b. %d, %Y at %I:%M%p'
    return date.strftime(format)
