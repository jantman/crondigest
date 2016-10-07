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
from crondigest.config import Config

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
            c = Config('/foo/bar.py')
        assert c.config_path == '/foo/bar.py'
        assert mock_load.mock_calls == [call(c)]

class TestConfig(object):

    def setup(self):
        with patch('%s._load_conf' % pb, autospec=True) as mock_load:
            self.cls = Config('/conf/path.py')

    def test_load_conf_SourceFileLoader(self):
        mock_sfl = Mock()
        mock_imp = Mock()
        with patch('%s._load_with_SourceFileLoader' % pb,
                   autospec=True) as mock_load_sfl:
            with patch('%s._load_with_imp' % pb,
                       autospec=True) as mock_load_imp:
                self.cls.have_SourceFileLoader = True
                mock_load_sfl.return_value = mock_sfl
                mock_load_imp.return_value = mock_imp
                res = self.cls._load_conf()
        assert res == mock_sfl
        assert mock_load_imp.mock_calls == []
        assert mock_load_sfl.mock_calls == [call(self.cls)]
