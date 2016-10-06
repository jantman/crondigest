"""
crondigest %VERSION% example configuration file
<%PROJECT_URL%>

Edit this file as necessary to configure crondigest. Its default path
is /etc/crondigest_conf.py but that can be overridden with the
-c / --config option to crondigest.
"""

# STATE_PATH is the directory where crondigest will store its state (i.e.
# output of runs, status, crontab copies, etc.). When SINGLE_USER is true,
# it must be world-writable.
STATE_PATH = '/var/cache/crondigest'

# When SINGLE_USER is set to True, all log files will be world-readable and
# crondigest will assume that all commands it runs on the system should have
# output and results sent to the same user (i.e. a system with a single human
# user).
SINGLE_USER = True

# MAILTO is a string or list of strings specifying email report recipients,
# like:
# MAILTO = ['root', 'me@example.com']
# or
# MAILTO = 'me@example.com'
MAILTO = 'root'
