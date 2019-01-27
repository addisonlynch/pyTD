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

import os
import re
import logging
import time
import requests
import subprocess

from pyTD import CONFIG_DIR
from pyTD import DEFAULT_SSL_DIR

from pyTD.auth import TDAuthManager
from pyTD.cache import DiskCache, MemCache
from pyTD.utils import yn_require, bprint, gprint, rprint, _init_session
from pyTD.utils.exceptions import (Redirection, ValidationError,
                                   AuthorizationError, ForbiddenAccess,
                                   ResourceNotFound, ClientError,
                                   ServerError, ConfigurationError,
                                   SSLError, TDQueryError)


logger = logging.getLogger(__name__)


def gen_ssl(config_dir):
    """
    Generates SSL certificate cert.pem and key key.pem, then places them in
    config_dir.

    Parameters
    ----------
    config_dir: str
        Absolute path to the desired output directory
    """
    COMMAND = ("openssl req -newkey rsa:2048 -nodes -keyout key.pem "
               "-x509 -days 365 -out cert.pem")
    logger.info("Generating SSL certificate and key in %s" % config_dir)
    if not os.path.exists(config_dir):
        raise SSLError("Configuration path: %s not found." % config_dir)
    os.chdir(config_dir)
    try:
        subprocess.check_call(COMMAND, shell=True)
    except subprocess.CalledProcessError:
        logger.error("Could not generate SSL certificate and key.")
        raise SSLError("Could not generate SSL certificate and key.")
    finally:
        logger.info("SSL certificate and key created successfully.")
        return True


def refresh_auth():
    global __api__
    if __api__ is None:
        raise AuthorizationError("Default API not found.")
    else:
        __api__.refresh_auth()
        return


class api(object):
    """ User agent for authenticated TD Ameritrade HTTP requests

    Attributes
    ----------
    options: dict, optional
        Pre-instantiated dictionary of options
    consumer_key: str
        Your application's OAuth ID
    callback_url: str
        Your application's Redirect URI
    store_tokens: bool, default True, optional
        Enables on-disk token cache if selected, which is default
        behavior. Disabled when access_token or refresh_token is
        passed
    cache: MemCache or DiskCache, optional
        A pre-instantiated token cache
    retry_count: int, default 3, optional
        Desired number of retries if a request fails
    pause: float, default 0.5, optional
        Pause time between retry attempts
    session: requests_cache.session, default None, optional
        A cached requests-cache session
    Examples
    --------

    >>> import pyTD
    >>> api = pyTD.api(consumer_key="TEST@AMER.OAUTHAP",
                       callback_url="https://localhost:8080")
    >>> api.market.get_quote("AAPL")
    """
    def __init__(self, options=None, **kwargs):
        """
        Initialize API object
        """
        kwargs.update(options or {})
        # Required parameters
        self.consumer_key = kwargs["consumer_key"]
        self.callback_url = kwargs["callback_url"]

        # Optional optional parameters
        self.retry_count = kwargs.get("retry_count", 3)
        self.pause = kwargs.get("pause", 0.5)
        self.session = _init_session(kwargs.get("session"))
        tokens = kwargs.get("store_tokens", True)
        self.store_tokens = os.getenv("TD_STORE_TOKENS", tokens)
        if self.store_tokens in [True, "true", "True"]:
            self.store_tokens = True
        elif self.store_tokens in [False, "false", "False"]:
            self.store_tokens = False
        else:
            raise ValueError("Enter True or False for store_tokens.")
        self.ssl_dir = DEFAULT_SSL_DIR
        self.ssl_cert_path = os.path.join(self.ssl_dir, 'cert.pem')
        self.ssl_key_path = os.path.join(self.ssl_dir, 'key.pem')
        self.cache = kwargs.get("cache")

        if self.cache is None:
            if self.store_tokens is True:
                self.cache = DiskCache(CONFIG_DIR, self.consumer_key)
            else:
                self.cache = MemCache()

        # Set up an authorization manager
        self.auth = TDAuthManager(self.cache, self.consumer_key,
                                  self.callback_url)
        # For debugging purposes
        self.options = kwargs

    def refresh_auth(self):
        if self.refresh_valid:
            choice = yn_require("Current authentication tokens appear to "
                                "be valid. Would you like to overwrite them?")
            if choice is False:
                return
        refresh_token, access_token = self.auth.auth_via_browser()
        self.cache.refresh_token = refresh_token
        self.cache.access_token = access_token

    @property
    def refresh_token(self):
        """Router to refresh token of cache"""
        return self.cache.refresh_token

    @property
    def access_token(self):
        """Router to access token of cache"""
        return self.cache.access_token

    @property
    def refresh_valid(self):
        """Validity of cache refresh token"""
        try:
            return self.refresh_token.valid
        except ConfigurationError:
            return False

    @property
    def access_valid(self):
        """Validity of cache access token"""
        try:
            return self.access_token.valid
        except ConfigurationError:
            return False

    @property
    def auth_valid(self):
        """Validity of refresh token and access token"""
        return self.refresh_valid and self.access_valid

    @property
    def headers(self):
        return {
            "content-type": "application/json"
        }

    @property
    def data(self):
        return {}

    def __str__(self):
        FMT = "API(consumer_key: %s, callback_url: %s, config: %s)"
        return FMT % (self.consumer_key, self.callback_url, CONFIG_DIR)

    def __repr__(self):
        FMT = "API(consumer_key: %s, callback_url: %s)\n"
        DEBUG = "ENV(CONSUMER_KEY: %s, CALLBACK_URL: %s, TD_CONFIG_DIR: %s)"
        MSG = FMT % (self.consumer_key, self.callback_url)
        DBG = DEBUG % (os.getenv("TD_CONSUMER_KEY"),
                       os.getenv("TD_CALLBACK_URL"),
                       os.getenv("TD_CONFIG_DIR"))
        return "%s%s" % (MSG, DBG)

    def request(self, method, url, **kwargs):
        headers = kwargs.pop("headers", self.headers)
        headers.update({'authorization': self._auth_header})
        params = kwargs.pop("params", None)
        params = params or {}
        params.update({"apikey": self.consumer_key})
        status_check = kwargs.pop("status", None)

        logger.debug("%s %s - %s" % (bprint("REQUEST:"), method, url))
        logger.debug("PARAMS: %s" % params)
        logger.debug("HEADERS: %s" % headers)

        if "data" in kwargs:
            logger.debug("BODY: %s" % kwargs["data"])

        # Try 3 times to obtain a response with a good status code
        for i in range(self.retry_count+1):
            response = self.session.request(method, url, headers=headers,
                                            params=params, **kwargs)
            if response.status_code == requests.codes.ok:
                return self.handle_response(response)
            time.sleep(self.pause)

        # Return the failed response anyway
        return self.handle_response(response, status_check)

    def get(self, url=None, params=None):
        response = self.request("GET", url=url, params=params)

        # Convert GET requests to JSON
        try:
            json_data = response.json()
        except ValueError:
            raise TDQueryError(message="An error occurred during the query.",
                               response=response)
        if "error" in json_data:
            raise TDQueryError(response=response)
        return json_data

    def post(self, url=None, params=None, data=None):
        response = self.request("POST", url, data=data)

        try:
            json_data = response.json()
        except ValueError:
            raise TDQueryError(message="An error occurred during the query.",
                               response=response)
        return json_data

    def _check_status_codes(self, response):
        status = response.status_code
        logger.debug("RESPONSE TEXT (1st 200 chars): %s" % response.text[:200])
        if status in [301, 302, 303, 307]:
            message = "There was an unexpected redirect during your request."
            raise Redirection(response, message=message)
        elif status == 400:
            message = "There was a validation problem with your request."
            raise ValidationError(response, message=message)
        elif status == 401:
            message = "Auth Token invalid."
            raise AuthorizationError(message)
        elif status == 403:
            message = "You are forbidden from accessing this resource."
            raise ForbiddenAccess(response, message=message)
        elif status == 404:
            message = "The requested resource was not found."
            raise ResourceNotFound(response=response, message=message)
        elif 401 <= status <= 499:
            message = "There was a client-side error with your request."
            raise ClientError(response, message=message)
        elif 500 <= status <= 599:
            t = response.text
            t = re.sub(r"[\n\t\s]*", "", t)
            t = re.sub(r"\\", "", t)
            try:
                import json
                json_data = json.loads(t)
                if json_data["error"] == "InvalidApiKey":
                    raise AuthorizationError("Invalid OAuth ID.")
            except ValueError:
                pass
            message = "There was a server-side error with your request."
            raise ServerError(response, message=message)
        else:
            raise TDQueryError(response=response,
                               message="Unknown response code.")

    def handle_response(self, response, status_check=None):
        # Ensures status code is OK
        logger.debug("REQUEST URL: %s" % response.url)
        status = response.status_code
        if status < 400:
            logger.debug("RESPONSE: %s" % gprint("%d" % response.status_code))
            return response
        else:
            logger.error("RESPONSE: %s" % bprint(rprint(str(status))))
            if status_check:
                status_check(response)
            return self._check_status_codes(response)

    @property
    def _auth_header(self):
        return "Bearer %s" % self.cache.access_token.token


__api__ = None


def default_api(ignore_globals=False):
    """ Attempts to read from environment variables

    Parameters
    ----------
    ignore_globals: boolean, default False
        Testing utility that forces creation of a new global API object
    """
    global __api__
    if ignore_globals is True:
        __api__ = None

    params = {}

    if __api__ is None:
        try:
            logger.debug("Attempting to read from the environment variables "
                         "TD_CONSUMER_KEY and TD_CALLBACK_URL")
            params['consumer_key'] = os.environ["TD_CONSUMER_KEY"]
            params['callback_url'] = os.environ["TD_CALLBACK_URL"]
            logger.debug("Creating api object from environment variables.")
            if ignore_globals is True:
                return api(**params)
            __api__ = api(**params)
            return __api__
        except KeyError:
            raise ConfigurationError("Environment variables not found.")
        else:
            raise ConfigurationError("No valid configuration found. Try "
                                     "pyTD.configure.")
    else:
        return __api__


def configure(options=None, **kwargs):
    """
    Create new api given configuration options

    Parameters
    ----------
    options: dict, optional
        A pre-instantiated argument dictionary
    consumer_key: str, optional
        OAuth ID of application
    callback_url: str, optional
        Redirect URI of application
    cache: str, optional
        Token cache (use for testing)
    """
    global __api__

    # Create configuration directory if it does not exist
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        logger.info("Created configuration directory %s" % CONFIG_DIR)
    else:
        logger.info("Configuration directory exists: %s" % CONFIG_DIR)

    # Next create SSL keys if they do not exist
    cert_path = os.path.join(DEFAULT_SSL_DIR, 'cert.pem')
    key_path = os.path.join(DEFAULT_SSL_DIR, 'key.pem')

    if not os.path.isfile(cert_path) or not os.path.isfile(key_path):
        if os.path.isdir(DEFAULT_SSL_DIR) is False:
            logger.debug("Creating directory %s to store SSL cert and "
                         "key" % DEFAULT_SSL_DIR)
            os.makedirs(DEFAULT_SSL_DIR)
            logger.debug("SSL directory %s created" % DEFAULT_SSL_DIR)
        else:
            logger.debug("SSL directory exists: %s" % DEFAULT_SSL_DIR)
        gen_ssl(DEFAULT_SSL_DIR)

    consumer_key = kwargs.get("consumer_key")
    callback_url = kwargs.get("callback_url")
    cache = kwargs.get("cache")

    if consumer_key and callback_url:
        os.environ["TD_CONSUMER_KEY"] = consumer_key
        os.environ["TD_CALLBACK_URL"] = callback_url

        __api__ = api(consumer_key=consumer_key,
                      callback_url=callback_url,
                      cache=cache)
    return __api__
