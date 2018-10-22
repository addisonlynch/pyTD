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

from pyTD.cache import MemCache
from pyTD.auth.tokens import EmptyToken


@pytest.fixture(scope='function', autouse=True)
def full_consumer_key():
    return "TEST@AMER.OAUTHAP"


class TestMemCache(object):

    def test_default_values(self):
        c = MemCache()

        assert isinstance(c.refresh_token, EmptyToken)
        assert isinstance(c.access_token, EmptyToken)

    def test_set_token(self, valid_refresh_token):
        c = MemCache()
        c.refresh_token = valid_refresh_token

        assert c.refresh_token.token == "validtoken"
        assert c.refresh_token.expires_in == 1000000

    def test_clear(self, valid_refresh_token, valid_access_token):
        c = MemCache()
        c.refresh_token = valid_refresh_token
        c.access_token == valid_access_token

        c.clear()
        assert isinstance(c.refresh_token, EmptyToken)
        assert isinstance(c.access_token, EmptyToken)
