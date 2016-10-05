crondigest
==========

A cron job wrapper to send batched digest email and notify of missed jobs.

Overview
--------

I run a bunch of cron job on my desktop computer; things like backups of cloud services and my home directory, hard drive health checks, etc. I want to know if they fail (or if they're not run), but I no longer have any desire to run a full-fledged monitoring system like Icinga.

``crondigest`` is a Python tool that wraps your cron jobs. It captures their STDOUT, STDERR, runtime and exit codes and stores them locally (it's intended for single-user machines like desktops and laptops, so it defaults to storing every user's cron information in the same file). It also parses the crontab file of every user that runs it, and stores a copy. When ``crondigest`` runs, if it hasn't done so within a configurable interval (stored in a state file), it generates and emails an HTML report of all jobs that have run since the last report, as well as any jobs that were listed in crontabs but didn't run.

The end result is (or should be) a daily email report of all cron jobs that ran (along with their status, runtime and output/error) as well as a listing of any jobs that should have run but didn't.
