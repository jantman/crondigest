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
import logging
import pytest
from inspect import getsource


from crondigest.runner import (parse_args, set_log_info, set_log_debug,
                               set_log_level_format, main)
from crondigest.version import VERSION, PROJECT_URL
import crondigest.example_config as example_config_module

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'crondigest.runner'


class TestMain(object):

    def test_example_config(self, capsys):
        expected = getsource(example_config_module)
        expected = expected.replace('%VERSION%', VERSION)
        expected = expected.replace('%PROJECT_URL%', PROJECT_URL)
        args = ['crondigest', '--example-config', 'foo']
        mock_args = Mock(verbose=0, config='cpath', example_config=True,
                         COMMAND='foo')
        with patch('%s.logger' % pbm, autospec=True) as mocklogger:
            with patch.multiple(
                pbm,
                autospec=True,
                set_log_info=DEFAULT,
                set_log_debug=DEFAULT,
                parse_args=DEFAULT,
            ) as mocks:
                mocks['parse_args'].return_value = mock_args
                with patch.object(sys, 'argv', args):
                    main()
        assert mocks['set_log_info'].mock_calls == []
        assert mocks['set_log_debug'].mock_calls == []
        assert mocks['parse_args'].mock_calls == [call(args[1:])]
        assert mocklogger.mock_calls == []
        out, err = capsys.readouterr()
        assert out == expected
        assert err == ''


class TestParseArgs(object):

    def test_parser(self):
        parsed = Mock(example_config=False, COMMAND=['foo'])
        with patch('%s.argparse.ArgumentParser' % pbm, autospec=True) as mock_p:
            mock_p.return_value.parse_args.return_value = parsed
            res = parse_args(['foo'])
        assert res == parsed
        assert mock_p.mock_calls == [
            call(description='crondigest - A cron job wrapper to send '
                             'batched digest email and notify of missed '
                             'jobs - <%s>' % PROJECT_URL),
            call().add_argument('-c', '--config', action='store',
                                default='/etc/crondigest_conf.py',
                                dest='config',
                                help='path to config file (default: '
                                     '/etc/crondigest_conf.py)',
                                type=str),
            call().add_argument('-v', '--verbose', action='count', default=0,
                                dest='verbose',
                                help='verbose output. specify twice for '
                                     'debug-level output.'),
            call().add_argument('-V', '--version', action='version',
                                version='crondigest v%s <%s>' % (
                                    VERSION, PROJECT_URL)),
            call().add_argument('--example-config', action='store_true',
                                default=False, dest='example_config',
                                help='print example config file content '
                                     'and exit'),
            call().add_argument('COMMAND', action='store',
                                help='cron command to run; must be '
                                     'shell-escaped and shouldbe quoted to '
                                     'act as one argument to crondigest',
                                nargs='*', type=str),
            call().parse_args(['foo']),
        ]

    def test_no_command(self, capsys):
        with pytest.raises(SystemExit) as excinfo:
            parse_args([])
        assert excinfo.value.code == 2
        out, err = capsys.readouterr()
        assert err == "ERROR: You must specify exactly one COMMAND argument.\n"
        assert out == ''

    def test_only_command(self):
        res = parse_args(['foo bar "baz" blam && blarg'])
        assert res.config == '/etc/crondigest_conf.py'
        assert res.verbose == 0
        assert res.example_config is False
        assert res.COMMAND == ['foo bar "baz" blam && blarg']

    def test_config(self):
        res = parse_args(['--config=/foo/bar', 'foo'])
        assert res.config == '/foo/bar'
        assert res.verbose == 0
        assert res.example_config is False
        assert res.COMMAND == ['foo']

    def test_verbose(self):
        res = parse_args(['-v', 'foo'])
        assert res.config == '/etc/crondigest_conf.py'
        assert res.verbose == 1
        assert res.example_config is False
        assert res.COMMAND == ['foo']

    def test_verbose2(self):
        res = parse_args(['-vv', 'foo'])
        assert res.config == '/etc/crondigest_conf.py'
        assert res.verbose == 2
        assert res.example_config is False
        assert res.COMMAND == ['foo']

    def test_version(self, capsys):
        with pytest.raises(SystemExit) as excinfo:
            parse_args(['-V'])
        assert excinfo.value.code == 0
        expected = "crondigest v%s <%s>\n" % (
            VERSION, PROJECT_URL
        )
        out, err = capsys.readouterr()
        if (sys.version_info[0] < 3 or
                (sys.version_info[0] == 3 and sys.version_info[1] < 4)):
            assert out == ''
            assert err == expected
        else:
            assert out == expected
            assert err == ''

    def test_example_config(self):
        res = parse_args(['--example-config'])
        assert res.config == '/etc/crondigest_conf.py'
        assert res.verbose == 0
        assert res.example_config is True
        assert res.COMMAND == []


class TestSetLog(object):

    def test_set_log_info(self):
        with patch('%s.set_log_level_format' % pbm) as mock_set:
            set_log_info()
        assert mock_set.mock_calls == [
            call(logging.INFO, '%(asctime)s %(levelname)s:%(name)s:%(message)s')
        ]

    def test_set_log_debug(self):
        with patch('%s.set_log_level_format' % pbm) as mock_set:
            set_log_debug()
        assert mock_set.mock_calls == [
            call(logging.DEBUG,
                 "%(asctime)s [%(levelname)s %(filename)s:%(lineno)s - "
                 "%(name)s.%(funcName)s() ] %(message)s")
        ]

    def test_set_log_level_format(self):
        mock_handler = Mock(spec_set=logging.Handler)
        with patch('%s.logger' % pbm) as mock_logger:
            with patch('%s.logging.Formatter' % pbm) as mock_formatter:
                type(mock_logger).handlers = [mock_handler]
                set_log_level_format(5, 'foo')
        assert mock_formatter.mock_calls == [
            call(fmt='foo')
        ]
        assert mock_handler.mock_calls == [
            call.setFormatter(mock_formatter.return_value)
        ]
        assert mock_logger.mock_calls == [
            call.setLevel(5)
        ]
