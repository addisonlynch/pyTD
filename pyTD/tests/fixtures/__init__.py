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

import pytest

from pyTD.auth.tokens import RefreshToken, AccessToken
from pyTD.cache import MemCache
from pyTD.utils import to_timestamp


valid_params = {
    "token": "validtoken",
    "access_time": to_timestamp(datetime.datetime.now()) - 15000,
    "expires_in": 1000000,
}

invalid_params = {
    "token": "invalidtoken",
    "access_time": to_timestamp(datetime.datetime.now()) - 15000,
    "expires_in": 10000,
}


@pytest.fixture(scope='function')
def valid_cache():
    r = RefreshToken(valid_params)
    a = AccessToken(valid_params)
    c = MemCache()
    c.refresh_token = r
    c.access_token = a
    return c


@pytest.fixture(scope='function')
def invalid_cache():
    r = RefreshToken(invalid_params)
    a = AccessToken(invalid_params)
    c = MemCache()
    c.refresh_token = r
    c.access_token = a
    return c


@pytest.fixture(scope='session')
def valid_refresh_token():
    return RefreshToken(valid_params)


@pytest.fixture(scope='session')
def valid_access_token():
    return AccessToken(valid_params)


@pytest.fixture(scope='session', autouse=True)
def sample_oid():
    return "TEST10@AMER.OAUTHAP"


@pytest.fixture(scope='session', autouse=True)
def sample_uri():
    return "https://127.0.0.1:60000/td-callback"


@pytest.fixture(scope="function")
def set_env(monkeypatch, sample_oid, sample_uri):
    monkeypatch.setenv("TD_CONSUMER_KEY", sample_oid)
    monkeypatch.setenv("TD_CALLBACK_URL", sample_uri)


@pytest.fixture(scope="function")
def del_env(monkeypatch):
    monkeypatch.delenv("TD_CONSUMER_KEY", raising=False)
    monkeypatch.delenv("TD_CALLBACK_URL", raising=False)
