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
import pytest
from mock import MagicMock

from pyTD.auth import TDAuthManager
from pyTD.cache import MemCache
from pyTD.auth.server import TDAuthServer
from pyTD.auth.tokens import EmptyToken, RefreshToken, AccessToken
from pyTD.utils.exceptions import AuthorizationError
from pyTD.utils.testing import MockResponse


@pytest.fixture(scope='function', autouse=True)
def sample_manager(sample_oid, sample_uri, valid_cache):
    def dummy(*args, **kwargs):
        return None
    c = MemCache()
    m = TDAuthManager(c, sample_oid, sample_uri)
    m._open_browser = dummy
    m._start_auth_server = dummy
    m._stop_auth_server = dummy
    return m


@pytest.fixture(scope='function')
def test_auth_response():
    return {
        "refresh_token": "TESTREFRESHVALUE",
        "refresh_token_expires_in": 7776000,
        "access_token": "TESTACCESSVALUE",
        "expires_in": 1800,
        "access_time": 1534976931
    }


@pytest.fixture(scope='function')
def test_auth_response_bad():
    return {
        "error": "Bad request"
    }


class TestAuth(object):

    def test_auth_init(self, sample_manager):

        assert isinstance(sample_manager.refresh_token, EmptyToken)
        assert isinstance(sample_manager.access_token, EmptyToken)

    def test_refresh_access_token_no_refresh(self, sample_manager):

        with pytest.raises(AuthorizationError):
            sample_manager.refresh_access_token()

    def test_auth_browser_fails(self, sample_manager, test_auth_response_bad):
        mock_server = MagicMock(TDAuthServer)
        mock_server._wait_for_tokens.return_value = test_auth_response_bad

        sample_manager.auth_server = mock_server

        with pytest.raises(AuthorizationError):
            sample_manager.auth_via_browser()

    def test_auth_browser_succeeds(self, sample_oid, sample_uri,
                                   sample_manager, monkeypatch,
                                   test_auth_response,
                                   valid_refresh_token,
                                   valid_access_token):
        mock_server = MagicMock(TDAuthServer)
        mock_server._wait_for_tokens.return_value = test_auth_response

        sample_manager.auth_server = mock_server

        r1, r2 = sample_manager.auth_via_browser()
        assert isinstance(r1, RefreshToken)
        assert isinstance(r2, AccessToken)
        assert r1.token == "TESTREFRESHVALUE"
        assert r2.token == "TESTACCESSVALUE"

    def test_auth_refresh_access_bad_token(self, invalid_cache, monkeypatch,
                                           mock_400, sample_oid, sample_uri):
        c = invalid_cache
        c.refresh_token.expires_in = 100000000000
        monkeypatch.setattr("pyTD.auth.manager.requests.post", lambda *a, **k:
                            mock_400)

        manager = TDAuthManager(c, sample_oid, sample_uri)
        with pytest.raises(AuthorizationError):
            manager.refresh_access_token()

    def test_auth_refresh_access(self, test_auth_response, monkeypatch,
                                 sample_oid, sample_uri, valid_cache):

        mocked_response = MockResponse(json.dumps(test_auth_response), 200)
        monkeypatch.setattr("pyTD.auth.manager.requests.post", lambda *a, **k:
                            mocked_response)

        manager = TDAuthManager(valid_cache, sample_oid, sample_uri)
        manager.refresh_access_token()
        assert manager.access_token.token == "TESTACCESSVALUE"
