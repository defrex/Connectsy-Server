from os import path

from fabric.api import *
from fabric.contrib.console import confirm

def server_pull():
    with cd('/var/www/api.dev.connectsy'):
        run('bzr pull /var/code/server/')
    print 'Server code updated'

def server_restart():
    run('sudo /etc/init.d/api.dev.connectsy restart ')
    print 'Server Restarted'
    
def server_update():
    server_pull()
    server_restart()

