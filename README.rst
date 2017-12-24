crondigest
==========

.. image:: http://www.repostatus.org/badges/latest/abandoned.svg
   :alt: Project Status: Abandoned – Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development.
   :target: http://www.repostatus.org/#abandoned

A cron job wrapper to send batched digest email and notify of missed jobs.

Deprecated and Abandoned
========================

See `ecsjobs <https://github.com/jantman/ecsjobs>`_ for my supported replacement.

Overview
--------

I run a bunch of cron job on my desktop computer; things like backups of cloud services and my home directory, hard drive health checks, etc. I want to know if they fail (or if they're not run), but I no longer have any desire to run a full-fledged monitoring system like Icinga.

``crondigest`` is a Python tool that wraps your cron jobs. It captures their STDOUT, STDERR, runtime and exit codes and stores them locally (it's intended for single-user machines like desktops and laptops, so it defaults to storing every user's cron information in the same file). It also parses the crontab file of every user that runs it, and stores a copy. When ``crondigest`` runs, if it hasn't done so within a configurable interval (stored in a state file), it generates and emails an HTML report of all jobs that have run since the last report, as well as any jobs that were listed in crontabs but didn't run.

The end result is (or should be) a daily email report of all cron jobs that ran (along with their status, runtime and output/error) as well as a listing of any jobs that should have run but didn't.

**Note** that in its current form, crondigest is designed for single (human)
user systems; the information on every command run and every user's crontab
will be stored in a single world-writable directory, and crondigest will effectively
act as though every user running it is the same.

Requirements
------------

* Python 2.7 or 3.3+ (currently tested with 2.7, 3.3, 3.4 and 3.5)
* Python `VirtualEnv <http://www.virtualenv.org/>`_ and ``pip`` (recommended installation method; your OS/distribution should have packages for these)

Installation
------------

It's recommended that you install into a virtual environment (virtualenv /
venv). See the `virtualenv usage documentation <http://www.virtualenv.org/en/latest/>`_
for information on how to create a venv.

.. code-block:: bash

    pip install crondigest

Configuration
-------------

Run ``crondigest --example-config`` to print an example config file to STDOUT;
edit this text as needed (see the comments inline for instructions) and save
as ``/etc/crondigest_conf.py``. The configuration file is imported as a Python
module, so you can use any Python code you need as long as you end up with the
variables documented.

Usage
-----

Quote your existing cron commands, and send them as the first argument to
``crondigest``.

i.e., an original crontab entry of:

.. code-block::

    0 2 * * * FOO=bar /home/username/bin/run_something.py -s nightly

becomes:

.. code-block::

    0 2 * * * crondigest 'FOO=bar /home/username/bin/run_something.py -s nightly'

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the `GitHub Issue Tracker <https://github.com/jantman/crondigest/issues>`_. Pull requests are
welcome. Issues that don't have an accompanying pull request will be worked on
as my time and priority allows.

Development
===========

To install for development:

1. Fork the `crondigest <https://github.com/jantman/crondigest>`_ repository on GitHub
2. Create a new branch off of master in your fork.

.. code-block:: bash

    $ virtualenv crondigest
    $ cd crondigest && source bin/activate
    $ pip install -e git+git@github.com:YOURNAME/crondigest.git@BRANCHNAME#egg=crondigest
    $ cd src/crondigest

The git clone you're now in will probably be checked out to a specific commit,
so you may want to ``git checkout BRANCHNAME``.

Guidelines
----------

* pep8 compliant with some exceptions (see pytest.ini)
* 100% test coverage with pytest (with valid tests)

Testing
-------

Testing is done via `pytest <http://pytest.org/latest/>`_, driven by `tox <http://tox.testrun.org/>`_.

* testing is as simple as:

  * ``pip install tox``
  * ``tox``

* If you want to pass additional arguments to pytest, add them to the tox command line after "--". i.e., for verbose pytext output on py27 tests: ``tox -e py27 -- -v``

Release Checklist
-----------------

1. Open an issue for the release; cut a branch off master for that issue.
2. Confirm that there are CHANGES.rst entries for all major changes.
3. Ensure that Travis tests passing in all environments.
4. Ensure that test coverage is no less than the last release (ideally, 100%).
5. Increment the version number in crondigest/version.py and add version and release date to CHANGES.rst, then push to GitHub.
6. Confirm that README.rst renders correctly on GitHub.
7. Upload package to testpypi:

   * Make sure your ~/.pypirc file is correct (a repo called ``test`` for https://testpypi.python.org/pypi)
   * ``rm -Rf dist``
   * ``python setup.py register -r https://testpypi.python.org/pypi``
   * ``python setup.py sdist bdist_wheel``
   * ``twine upload -r test dist/*``
   * Check that the README renders at https://testpypi.python.org/pypi/crondigest

8. Create a pull request for the release to be merged into master. Upon successful Travis build, merge it.
9. Tag the release in Git, push tag to GitHub:

   * tag the release. for now the message is quite simple: ``git tag -a X.Y.Z -m 'X.Y.Z released YYYY-MM-DD'``
   * push the tag to GitHub: ``git push origin X.Y.Z``

11. Upload package to live pypi:

    * ``twine upload dist/*``

10. make sure any GH issues fixed in the release were closed.
