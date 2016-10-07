"""
crondigest %VERSION% example configuration file
<%PROJECT_URL%>

Edit this file as necessary to configure crondigest. Its default path
is /etc/crondigest_conf.py but that can be overridden with the
-c / --config option to crondigest.
"""

from datetime import timedelta

# STATE_PATH is the directory where crondigest will store its state (i.e.
# output of runs, status, crontab copies, etc.). When SINGLE_USER is true,
# it must be world-writable.
STATE_PATH = '/var/cache/crondigest'

# MAILTO is a string or list of strings specifying email report recipients,
# like:
# MAILTO = ['root', 'me@example.com']
# or
# MAILTO = 'me@example.com'
MAILTO = 'root'

# This defines how often mail should be sent (i.e. if mail has not been sent
# in this amount of time, send it now). This is a ``datetime.timedelta``.
MAIL_INTERVAL = timedelta(days=1)

# This defines how long to keep logs/output/results from commands run.
LOG_RETENTION = timedelta(days=7)
