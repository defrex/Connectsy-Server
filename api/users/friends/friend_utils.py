import db
import status

def friend_status(from_user, to):
    '''
    Gets from status from one user to another
    '''
    friend_status = db.objects.friend.find_one({u'from': from_user, u'to': to})
    if friend_status:
        friend_status = friend_status[u'status']
        if friend_status == status.PENDING:
            friend_status = status.PENDING_TO
    else:
        friend_status = db.objects.friend.find_one({u'to': from_user, u'from': to})
        if friend_status:
            friend_status = friend_status[u'status']
            if friend_status == status.PENDING:
                friend_status = status.PENDING_FROM
    if not friend_status:
        friend_status = status.NOT_FRIEND

    return friend_status

def get_friends(user):
    '''
    Gets a list of usernames of the user's friends
    '''
    return [friend[u'to'] for friend in db.objects.friend.find({u'from': user, u'status': status.ACCEPTED})] + \
           [friend[u'from'] for friend in db.objects.friend.find({u'to': user, u'status': status.ACCEPTED})]

