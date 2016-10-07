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

import logging
import os
from datetime import timedelta

have_SourceFileLoader = False
try:  # nocoverage
    # Python 3.3+
    from importlib.machinery import SourceFileLoader
    have_SourceFileLoader = True
except ImportError:
    import imp
    have_SourceFileLoader = True

logger = logging.getLogger(__name__)


class Config(object):

    def __init__(self, config_path):
        """
        Initialize the Config, using the configuration module at the specified
        filesystem path.

        :param config_path: filesystem path to the config module
        :type config_path: str
        """
        self.config_path = os.path.abspath(os.path.expanduser(config_path))
        logger.debug('Configuration module path: %s', self.config_path)
        self._load_conf()

    def _load_conf(self):
        """
        Load configuration from ``self.config_path``; set instance variables.
        """
        if have_SourceFileLoader:
            conf_mod = self._load_with_SourceFileLoader()
        else:
            conf_mod = self._load_with_imp()
        # make dict and return

    def _load_with_SourceFileLoader(self):
        """
        Load configuration module using ``importlib.machinery.SourceFileLoader``

        :return: crondigest config file module
        :rtype: module
        """
        logger.debug(
            'Loading config using importlib.machinery.SourceFileLoader()'
        )
        mod = SourceFileLoader(
            'crondigest_conf', self.config_path).load_module()
        return mod

    def _load_with_imp(self):
        """
        Load configuration module using ``imp.load_source``

        :return: crondigest config file module
        :rtype: module
        """
        logger.debug('Loading config using imp.load_source()')
        mod = imp.load_source('crondigest_conf', self.config_path)
        return mod
