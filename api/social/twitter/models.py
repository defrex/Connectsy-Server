from db.models import Model


class TwitterAuth(Model):
    __collection__ = 'twitter_auth'
    __fields__ = {
        u'token': None,
        u'secret': None,
        u'username': None,
    }
