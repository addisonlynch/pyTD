# MIT License

# Copyright (c) 2018 Addison Lynch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import logging
import os

from pyTD.auth.tokens import AccessToken, RefreshToken
from pyTD.cache.base import TokenCache
from pyTD.utils.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class DiskCache(TokenCache):
    """
    On-disk token cache for access and refresh tokens

    Attributes
    ----------
    config_dir: str
        Desired directory to store cache
    filename: str
        Desired cache file name

    Usage
    -----

        >>> c = DiskCache()
        >>> c.refresh_token = token
        >>> c.access_token = token
    """
    def __init__(self, config_dir, filename):
        self.config_dir = os.path.expanduser(config_dir)
        if not os.path.isdir(self.config_dir):
            raise ConfigurationError("Directory %s not found. Configuration "
                                     "likely incomplete. "
                                     "Try pyTD.configure()" % self.config_dir)
        self.filename = filename
        self.config_path = os.path.join(self.config_dir, self.filename)
        self._create()

    def clear(self):
        """
        Empties the cache, though does not delete the cache file
        """
        with open(self.config_path, 'w') as f:
            json_data = {
                "refresh_token": None,
                "access_token": None,
            }
            f.write(json.dumps(json_data))
            f.close()
        return

    def _create(self):
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                json_data = {
                    "refresh_token": None,
                    "access_token": None,
                }
                f.write(json.dumps(json_data))
                f.close()
        return

    def _exists(self):
        """
        Utility function to test whether the configuration exists
        """
        return os.path.isfile(self.config_path)

    def _get(self, value=None):
        """
        Retrieves configuration information. If not passed a parameter,
        returns all configuration as a dictionary

        Parameters
        ----------
        value: str, optional
            Desired configuration value to retrieve
        """
        if self._exists() is True:
            f = open(self.config_path, 'r')
            config = json.load(f)
            if value is None:
                return config
            elif value not in config:
                raise ValueError("Value %s not found in configuration "
                                 "file." % value)
            else:
                if value == "refresh_token" and config[value]:
                    return RefreshToken(config[value])
                elif value == "access_token" and config[value]:
                    return AccessToken(config[value])
                else:
                    return config[value]
        else:
            raise ConfigurationError("Configuration file not found in "
                                     "%s." % self.config_path)

    def _set(self, attr, payload):
        """
        Update configuration file given payload

        Parameters
        ----------
        payload: dict
            Dictionary of updated configuration variables
        """
        with open(self.config_path) as f:
            json_data = json.load(f)
            f.close()
        json_data.update({attr: payload.__dict__()})
        with open(self.config_path, "w") as f:
            f.write(json.dumps(json_data))
            f.close()
            return True
        raise ConfigurationError("Could not update config file")
