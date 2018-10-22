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

import datetime
import logging
import requests
import webbrowser

from pyTD.auth.server import TDAuthServer
from pyTD.auth.tokens import RefreshToken, AccessToken
from pyTD.utils import to_timestamp
from pyTD.utils.exceptions import AuthorizationError

logger = logging.getLogger(__name__)


class TDAuthManager(object):
    """
    Authorization manager for TD Ameritrade OAuth 2.0 authorization and
    authentication.

    Attributes
    ----------
    auth_server: TDAuthServer or None
        An authentication server instance which can be started and stopped for
        handling authentication redirects.
    """
    def __init__(self, token_cache, consumer_key, callback_url):
        """
        Initialize the class

        Parameters
        ----------
        token_cache: MemCache or DiskCache
            A cache for storing the refresh and access tokens
        consumer_key: str
            Client OAuth ID
        callback_url: str
            Client Redirect URI
        """
        self.cache = token_cache
        self.consumer_key = consumer_key
        self.callback_url = callback_url
        self.auth_server = None

    @property
    def access_token(self):
        return self.cache.access_token

    @property
    def refresh_token(self):
        return self.cache.refresh_token

    def auth_via_browser(self):
        """
        Handles authentication and authorization.

        Raises
        ------
        AuthorizationError
            If the authentication or authorization could not be completed
        """
        self._start_auth_server()
        self._open_browser(self.callback_url)
        logger.debug("Waiting for authorization code...")
        tokens = self.auth_server._wait_for_tokens()
        self._stop_auth_server()

        try:
            refresh_token = tokens["refresh_token"]
            refresh_expiry = tokens["refresh_token_expires_in"]
            access_token = tokens["access_token"]
            access_expiry = tokens["expires_in"]
            access_time = tokens["access_time"]
        except KeyError:
            logger.error("Authorization could not be completed.")
            raise AuthorizationError("Authorization could not be completed.")
        r = RefreshToken(token=refresh_token, access_time=access_time,
                         expires_in=refresh_expiry)
        a = AccessToken(token=access_token, access_time=access_time,
                        expires_in=access_expiry)
        logger.debug("Refresh and Access tokens received.")
        return (r, a,)

    def _open_browser(self, url):
        logger.info("Opening browser to %s" % url)
        webbrowser.open(url, new=2)
        return True

    def refresh_access_token(self):
        """
        Attempts to refresh access token if current is not valid.

        Updates the cache if new token is received.

        Raises
        ------
        AuthorizationError
            If the access token is not successfully refreshed
        """
        if self.cache.refresh_token.valid is False:
            raise AuthorizationError("Refresh token is not valid.")
        logger.debug("Attempting to refresh access token...")
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'refresh_token',
                'refresh_token': self.cache.refresh_token.token,
                'client_id': self.consumer_key}
        try:
            authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/'
                                      'token', headers=headers, data=data)
            now = to_timestamp(datetime.datetime.now())
            if authReply.status_code == 400:
                raise AuthorizationError("Could not refresh access token.")
            authReply.raise_for_status()
            json_data = authReply.json()
            token = json_data["access_token"]
            expires_in = json_data["expires_in"]
        except (KeyError, ValueError):
            logger.error("Error retrieving access token.")
            raise AuthorizationError("Error retrieving access token.")
        access_token = AccessToken(token=token, access_time=now,
                                   expires_in=expires_in)
        logger.debug("Successfully refreshed access token.")
        self.cache.access_token = access_token

    def _start_auth_server(self):
        logger.info("Starting authorization server")

        # Return if server is already running
        if self.auth_server is not None:
            return
        self.auth_server = TDAuthServer(self.consumer_key, self.callback_url)

    def _stop_auth_server(self):
        logger.info("Shutting down authorization server")
        if self.auth_server is None:
            return
        self.auth_server = None
