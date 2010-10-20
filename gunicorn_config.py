import os

# let the processes scale up with the CPU cores
def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

workers = numCPUs() * 2 + 1

bind = "127.0.0.1:8000"

# see http://gunicorn.org/design.html
worker_class = 'tornado'

daemon = True

logfile = '/var/log/connectsy-server.log'

# process name in top, ps, etc
proc_name = 'connectsy-server'