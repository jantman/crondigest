# Notes

* output/status should be stored in files under a directory; simple for other things to parse and safe for multiple concurrent runs
* touch a lockfile every time we send an email
* capture exit code, runtime, stdout, stderr, ENV
  * should we worry about also streaming the command's stdout and stderr out of our process?
  * how do we capture stdout and stderr in a way that we can separate them in our email reports? line-based? look at how other things do it? (maybe TravisCI?)
* email should be nicely-formatted; nice CSS, show output in an expandable box with OUT and ERR separated; header rows should just show command, runtime, exit code (green or red background depending on exit code) with an arrow to expand
* every run should run the command, save metadata, save a copy of the user's crontab, then check for last send time and send email if needed (using a lockfile to try and prevent multiple processes from sending mail)
* config file should default to /etc/crondigest.py, overridable with ``-c``. Contains all config code including how to send email, multi-user mode, destination address, etc.
* cli should be: ``crondigest [options] 'command'`` where ``command`` is passed literally to a shell
* in default multi-user mode, files on disk should be world-readable so anyone can send the email. make this clear.
* ``--example-config`` dumps example config content (source of ``example_config.py`` in package)
* use instructions
  * at the top of each user's ``crontab``, ``MAILTO=""`` to disable built-in cron email
  * install globally with pip
  * commands now like: ``crondigest 'original_command'``
* Puppet module to install and configure, with a defined type to wrap cron tasks in ``crondigest``
* inspired by (maybe look at for ideas - BSD-licensed) https://pypi.python.org/pypi/cronwrap / https://github.com/Doist/cronwrap
* maybe build in single-run locking (``--lock``) like https://github.com/crustymonkey/cron-wrap
* example use case: nightly SSD/disk health checking
  * SMART
  * http://unix.stackexchange.com/questions/106678/how-to-check-the-life-left-in-ssd-or-the-mediums-wear-level
  * need a parsing/alerting script for these (some other tool for this?)
  * https://scottlinux.com/2014/07/15/determine-remaining-ssd-life-in-linux/
