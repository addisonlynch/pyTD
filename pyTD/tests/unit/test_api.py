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

import pytest
import subprocess

from pyTD.api import api, default_api, gen_ssl
from pyTD.utils.exceptions import (SSLError, ConfigurationError,
                                   ValidationError, AuthorizationError,
                                   ForbiddenAccess, ResourceNotFound,
                                   ClientError, ServerError)
from pyTD.utils.testing import MockResponse


@pytest.fixture(params=[
    (400, ValidationError),
    (401, AuthorizationError),
    (403, ForbiddenAccess),
    (404, ResourceNotFound),
    (450, ClientError),
    (500, ServerError)
])
def bad_requests(request):
    return request.param


class TestAPI(object):

    def test_non_global_api(self, sample_oid, sample_uri):

        a = api(consumer_key=sample_oid, callback_url=sample_uri)

        assert a.consumer_key == sample_oid
        assert a.callback_url == sample_uri

        assert a.refresh_valid is False
        assert a.access_valid is False
        assert a.auth_valid is False

    def test_api_passed_dict(self, sample_oid, sample_uri, valid_cache):
        params = {
            "consumer_key": sample_oid,
            "callback_url": sample_uri,
            "cache": valid_cache
        }

        a = api(params)

        assert a.consumer_key == sample_oid
        assert a.callback_url == sample_uri

        assert a.refresh_valid is True
        assert a.access_valid is True
        assert a.auth_valid is True

    def test_api_no_ssl(self, monkeypatch, sample_oid, sample_uri):

        monkeypatch.setattr('os.path.isfile', lambda x: False)

        with pytest.raises(SSLError):
            api(consumer_key=sample_oid, callback_url=sample_uri)


class TestDefaultAPI(object):

    def test_default_api(self, sample_oid, sample_uri, set_env):

        a = default_api(ignore_globals=True)

        assert a.consumer_key == sample_oid
        assert a.callback_url == sample_uri

        assert a.refresh_valid is False
        assert a.access_valid is False
        assert a.auth_valid is False

    def test_default_api_no_env(self, del_env):

        with pytest.raises(ConfigurationError):
            default_api(ignore_globals=True)


class sesh(object):

    def __init__(self, response):
        self.response = response

    def request(self, *args, **kwargs):
        return self.response


class TestAPIRequest(object):

    def test_api_request_errors(self, bad_requests):
        mockresponse = MockResponse("Error", bad_requests[0])
        m_api = default_api(ignore_globals=True)

        m_api.session = sesh(mockresponse)

        with pytest.raises(bad_requests[1]):
            m_api.request("GET", "https://none.com")

    def test_bad_oid_request(self):
        mockresponse = MockResponse('{"error": "Invalid ApiKey"}', 500)
        api = default_api(ignore_globals=True)

        api.session = sesh(mockresponse)

        with pytest.raises(AuthorizationError):
            api.request("GET", "https://none.com")


class TestGenSSL(object):

    def test_gen_ssl_pass(self, monkeypatch):
        monkeypatch.setattr("pyTD.api.subprocess.check_call",
                            lambda *a, **k: True)
        monkeypatch.setattr("pyTD.api.os.chdir", lambda *a, **k: None)
        assert gen_ssl(".") is True

    @pytest.mark.skip
    def test_gen_ssl_raises(self, monkeypatch):
        def mocked_check_call(*args, **kwargs):
            raise subprocess.CalledProcessError(1, "openssl")

        monkeypatch.setattr("pyTD.api.subprocess.check_call",
                            mocked_check_call)
        monkeypatch.setattr("pyTD.api.os.chdir", lambda *a, **k: None)

        with pytest.raises(SSLError):
            gen_ssl("/path/to/dir")
