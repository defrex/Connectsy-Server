import os
site_dir = os.path.dirname(__file__)
static_path = os.path.join(site_dir, "static")

# Global password salt
SALT = '0x3l33u3c2YNNxgJarYTiYukhj5NhyJ7b21kVoL2M8RZuhT91J28t1vkzceAyeB'

# Port to serve on
PORT = 8080

# MongoDB database name
DB_NAME = 'consy'

# is true, the tests are run rather then the server
TEST = False
TEST_DB = 'consy_testing'

# When these are set to None, the MongoDB defaults are used.  Override
# these values in your local settings if your database server runs on
# a non-local machine or a non-standard port.
DB_HOST = None
DB_PORT = None

TWILIO_ACCOUNT_SID = "ACc809eb42ff3bfe0160cb5bd720241a28"
TWILIO_AUTH_TOKEN = "426aeb9a2fabda0278b47fb36f84c8c6"
TWILIO_API_VERION = "2010-04-01"
TWILIO_NUMBERS = (
    '15126074649', # Austin
    '14155708208', # San Fran
    '16466005056', # New York
    #'+13108959876', # L.A.
    #'+16178703861', # Boston
)

DEBUG = False

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

