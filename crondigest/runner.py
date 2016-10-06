"""
The latest version of this package is available at:
<http://github.com/jantman/crondigest>

################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of crondigest.

    crondigest is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    crondigest is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with crondigest.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/crondigest> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

import sys
import argparse
import logging
from inspect import getsource

from crondigest.version import VERSION, PROJECT_URL
import crondigest.example_config as example_config_module

FORMAT = "[%(asctime)s %(levelname)s] %(message)s"
logging.basicConfig(level=logging.WARNING, format=FORMAT)
logger = logging.getLogger()


def parse_args(argv):
    """
    Use Argparse to parse command-line arguments.

    :param argv: list of arguments to parse (``sys.argv[1:]``)
    :type argv: list
    :return: parsed arguments
    :rtype: :py:class:`argparse.Namespace`
    """
    p = argparse.ArgumentParser(
        description='crondigest - A cron job wrapper to send batched digest '
                    'email and notify of missed jobs - <%s>' % PROJECT_URL
    )
    p.add_argument('-c', '--config', dest='config', type=str,
                   action='store', default='/etc/crondigest_conf.py',
                   help='path to config file '
                        '(default: /etc/crondigest_conf.py)')
    p.add_argument('-v', '--verbose', dest='verbose', action='count',
                   default=0,
                   help='verbose output. specify twice for debug-level output.')
    p.add_argument('-V', '--version', action='version',
                   version='crondigest v%s <%s>' % (
                       VERSION, PROJECT_URL
                   ))
    p.add_argument('--example-config', dest='example_config',
                   action='store_true', default=False,
                   help='print example config file content and exit')
    p.add_argument('COMMAND', type=str, action='store',
                   help='cron command to run; must be shell-escaped')
    args = p.parse_args(argv)
    return args


def set_log_info():
    """set logger level to INFO"""
    set_log_level_format(logging.INFO,
                         '%(asctime)s %(levelname)s:%(name)s:%(message)s')


def set_log_debug():
    """set logger level to DEBUG, and debug-level output format"""
    set_log_level_format(
        logging.DEBUG,
        "%(asctime)s [%(levelname)s %(filename)s:%(lineno)s - "
        "%(name)s.%(funcName)s() ] %(message)s"
    )


def set_log_level_format(level, format):
    """
    Set logger level and format.

    :param level: logging level; see the :py:mod:`logging` constants.
    :type level: int
    :param format: logging formatter format string
    :type format: str
    """
    formatter = logging.Formatter(fmt=format)
    logger.handlers[0].setFormatter(formatter)
    logger.setLevel(level)


def main(args=None):
    """
    Main entry point
    """
    # parse args
    if args is None:
        args = parse_args(sys.argv[1:])

    # dump example config if that action
    if args.example_config:
        src = getsource(example_config_module)
        src = src.replace('%VERSION%', VERSION)
        src = src.replace('%PROJECT_URL%', PROJECT_URL)
        sys.stdout.write(src)
        return

    # set logging level
    if args.verbose > 1:
        set_log_debug()
    elif args.verbose == 1:
        set_log_info()


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
