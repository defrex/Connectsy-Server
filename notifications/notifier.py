'''
Push notification handler class.

For documentation, see the included docstrings and the Android 2.2 (Froyo)
push notification implementation.
'''

# Typo preserved for humor's sake.  It was a George Bush moment.
#class Notificater(object):

class Notifier(object):
    '''
    This is an abstract class that should be inherited by the notifiers
    for each notification type.  If you want to add a new notification type,
    do the following (where foobar is the type):
    
    Create a module /notifications/clients/foobar.py
    In that module, define a class Notifier that inherits from this Notifier.
    
    That Notifier class can override any methods defined in this base class.
    Additionally, if setup work has to be performed (e.g. registering with
    a service somewhere, initializing a long poll, etc), it should be done
    in that subclass's __init__ method.
    
    Note that Notifier classes for some client types may be responsible for
    handling client "disconnections" (or whatever the appropriate shutdown
    mechanism is) from the push notification service.  If this is the case,
    the Notifier should also handle removing the appropriate database
    records as well.
    
    The notification system attempts to behave nicely when shutting down
    notifiers.  In the event of a proper shutdown, the destructors on all
    Notifier objects are guaranteed to be called, and as such they should
    be able to perform any cleanup actions in the __del__ method.  However,
    abnormal exits (caused by signals, Python internal errors, or os._exit)
    will skip this cleanup, and so a well-behaved Notifier should be
    prepared to deal with the consequences of an abnormal shutdown.
    '''
    
    def send(self, user, client_id, message_data):
        '''
        Sends a message to a client with the given ID.  The supplied
        `client_id` and `user` arguments can be used to pull a unique
        notification_reg record from the database, and are guaranteed to
        be valid for the Notifier's client type.
        
        This method should be prepared to handle any issues revolving
        around race conditions.  For example, for a Froyo notification
        the client_id points to the registration_id, which may be
        periodically invalidated by C2DM service.  It is possible that
        this invalidation will occur while the send method is in the
        process of being invoked, which would result in an error being
        returned by the service.  As such, the send method should handle
        this case gracefully.
        
        Note that some clients may not support all message types.  If the
        send method is passed message_data with an unsupported message type
        it should silently fail.
        '''
        raise Exception('Danger Will Robinson!  This Notifier (for client ' +
        'type "%s") lacks a send method.' % self.__module__)
        
    
        
    
    