"""
The latest version of this package is available at:
<http://github.com/jantman/crondigest>

##################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of crondigest, also known as crondigest.

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
##################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/crondigest> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
##################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
##################################################################################
"""

import sys
import pytest
from crondigest.config import Config
from datetime import timedelta

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'crondigest.config'
pb = '%s.Config' % pbm


class TestConfigInit(object):

    def test_init(self):
        with patch('%s._load_conf' % pb, autospec=True) as mock_load:
            mock_load.return_value = {'foo': 'bar'}
            c = Config('/foo/bar.py')
        assert c.config_path == '/foo/bar.py'
        assert mock_load.mock_calls == [call(c)]
        assert c._config == {'foo': 'bar'}


class TestConfig(object):

    def setup(self):
        with patch('%s._load_conf' % pb, autospec=True):
            self.cls = Config('/conf/path.py')

    def test_load_conf_SourceFileLoader(self):
        mock_sfl = Mock(FOO='bar', BA_Z='blam', _foo='bad')
        mock_imp = Mock(OOF='rab', Z_AB='malb', _bar='bad')
        with patch('%s._load_with_SourceFileLoader' % pb,
                   autospec=True) as mock_load_sfl:
            with patch('%s._load_with_imp' % pb,
                       autospec=True) as mock_load_imp:
                mock_load_sfl.return_value = mock_sfl
                mock_load_imp.return_value = mock_imp
                with patch('%s.have_SourceFileLoader' % pbm, True):
                    res = self.cls._load_conf()
        assert res == {'FOO': 'bar', 'BA_Z': 'blam'}
        assert mock_load_imp.mock_calls == []
        assert mock_load_sfl.mock_calls == [call(self.cls)]

    def test_load_conf_imp(self):
        mock_sfl = Mock(FOO='bar', BA_Z='blam', _foo='bad')
        mock_imp = Mock(OOF='rab', Z_AB='malb', _bar='bad')
        with patch('%s._load_with_SourceFileLoader' % pb,
                   autospec=True) as mock_load_sfl:
            with patch('%s._load_with_imp' % pb,
                       autospec=True) as mock_load_imp:
                mock_load_sfl.return_value = mock_sfl
                mock_load_imp.return_value = mock_imp
                with patch('%s.have_SourceFileLoader' % pbm, False):
                    res = self.cls._load_conf()
        assert res == {'OOF': 'rab', 'Z_AB': 'malb'}
        assert mock_load_imp.mock_calls == [call(self.cls)]
        assert mock_load_sfl.mock_calls == []

    @pytest.mark.skipif(sys.version_info < (3, 3), reason='test for py3.3+')
    def test_load_with_SourceFileLoader(self):
        mod = Mock()
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            with patch('%s.SourceFileLoader' % pbm, autospec=True) as mock_sfl:
                mock_sfl.return_value.load_module.return_value = mod
                res = self.cls._load_with_SourceFileLoader()
        assert res == mod
        assert mock_sfl.mock_calls == [
            call('crondigest_conf', '/conf/path.py'),
            call().load_module()
        ]
        assert mock_logger.mock_calls == [
            call.debug(
                'Loading config using importlib.machinery.SourceFileLoader()'
            )
        ]

    @pytest.mark.skipif(sys.version_info >= (3, 3), reason='test for py < 3.3')
    def test_load_with_imp(self):
        mod = Mock()
        with patch('%s.logger' % pbm, autospec=True) as mock_logger:
            with patch('%s.imp.load_source' % pbm, autospec=True) as mock_load:
                mock_load.return_value = mod
                res = self.cls._load_with_imp()
        assert res == mod
        assert mock_load.mock_calls == [
            call('crondigest_conf', '/conf/path.py')
        ]
        assert mock_logger.mock_calls == [
            call.debug('Loading config using imp.load_source()')
        ]

    def test_get(self):
        self.cls._config = {'bar': 123}
        assert self.cls.get('bar') == 123

    def test_print_config(self, capsys):
        self.cls._config = {
            'FOO': 'bar',
            'BAR': 123,
            'BAZ': True,
            'BL_AM': timedelta(days=7)
        }
        expected = "# crondigest effective configuration:\n"
        expected += "BAR = 123\n"
        expected += "BAZ = True\n"
        expected += "BL_AM = datetime.timedelta(7)\n"
        expected += "FOO = 'bar'\n"
        self.cls.print_config()
        out, err = capsys.readouterr()
        assert err == ''
        assert out == expected
