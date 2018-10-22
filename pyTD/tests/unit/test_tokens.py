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

from pyTD.auth.tokens import RefreshToken, AccessToken, EmptyToken
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


@pytest.fixture(params=[
        RefreshToken,
        AccessToken
    ], ids=["Refresh", "Access"], scope='function')
def tokens(request):
    return request.param


@pytest.fixture(params=[
        (valid_params, True),
        (invalid_params, False)
    ], ids=["valid", "invalid"])
def validity(request):
    return request.param


class TestTokens(object):

    def test_empty_token(self):
        t = EmptyToken()

        assert t.valid is False

    def test_new_token_dict_validity(self, tokens, validity):
        t = tokens(validity[0])

        assert t.valid is validity[1]

        assert t.token == validity[0]["token"]
        assert t.access_time == validity[0]["access_time"]
        assert t.expires_in == validity[0]["expires_in"]

    def test_new_token_params_validity(self, tokens, validity):
        t = tokens(**validity[0])

        assert t.valid is validity[1]

        assert t.token == validity[0]["token"]
        assert t.access_time == validity[0]["access_time"]
        assert t.expires_in == validity[0]["expires_in"]

    def test_token_equality(self, valid_refresh_token):
        token1 = RefreshToken(token="token", access_time=1, expires_in=1)
        token2 = RefreshToken({"token": "token", "access_time": 1,
                               "expires_in": 1})
        assert token1 == token2
