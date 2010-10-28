
from copy import copy
from db.models import Model

class GenericPollNotifications(Model):
    __collection__ = 'generic_poll_client'
    __fields__ = {
        u'client_id': None,
        u'notifications': list(),
    }
    
    @staticmethod
    def pop(client_id):
        record = GenericPollNotifications.get({u'client_id': client_id})
        if record is None: return None
        
        notifications = copy(record[u'notifications'])
        record[u'notifications'] = list()
        record.save()
        return notifications
        


