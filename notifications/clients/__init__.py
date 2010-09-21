import atexit

notifiers = {}

def import_client(name):
    global notifiers
    notifiers[name] = __import__(name, globals(), locals(), [], -1).Notifier()
    def cleanup():
        del notifiers[name]
    atexit.register(cleanup)
    
# import clients here
import_client('android_froyo')
import_client('generic_poll')