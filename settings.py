import os
site_dir = os.path.dirname(__file__)
static_path = os.path.join(site_dir, "static")

# Global password salt
SALT = '0x3l33u3c2YNNxgJarYTiYukhj5NhyJ7b21kVoL2M8RZuhT91J28t1vkzceAyeB'

# Port to serve on
PORT = 8080

# MongoDB database name
DB_NAME = 'consy'

# When these are set to None, the MongoDB defaults are used.  Override
# these values in your local settings if your database server runs on
# a non-local machine or a non-standard port.
DB_HOST = None
DB_PORT = None


# This is at the bottom so as to override anything we set here
from settings_local import *

'''
Local Settings
==============

Required
--------
DEVELOPMENT - True or False

Optional
--------
PROCESS_COUNT - Integer number of processes to use in prod
'''

