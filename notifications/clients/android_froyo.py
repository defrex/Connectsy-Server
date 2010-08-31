from notifications import notifier

class Notifier(notifier.Notifier):
    def __init__(self):
        #todo - one-time init
        pass
    
    def __del__(self):
        #todo - cleanup
        pass
        
    def send(self, user, client_id, message):
        #todo - send a message
        pass
        