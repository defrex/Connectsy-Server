from db.models import Model

class Friend(Model):
    __collection__ = 'friend'
    __fields__ = {
        u'from': None,
        u'to': None,
        u'status': None,
    }
    




