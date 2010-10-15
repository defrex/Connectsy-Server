from db.models import Model
from utils import timestamp

class NotificationRegister(Model):
    __collection__ = 'notification_reg'
    __fields__ = {
        u'user': None,
        u'timestamp': timestamp(),
        u'client_type': None,
        u'client_id': None,
        u'client_extra': None, #the client_extra field is optional
    }
    
    def save(self, safe=False):
        # update or insert based on 'client_id' being unique
        id = str(self.collection().update({u'client_id': self[u'client_id']}, 
                                          self.__data__, 
                                          safe=safe,
                                          upsert=True))
        if id is not None:
            self[u'id'] = id

    


