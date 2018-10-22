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

from pyTD.api import api
from pyTD.auth.tokens import EmptyToken
from pyTD.cache import MemCache


class TestAPICache(object):

    def test_api_init_cache(self, set_env, sample_oid, sample_uri):
        a = api(consumer_key=sample_oid, callback_url=sample_uri,
                store_tokens=False)

        assert isinstance(a.cache, MemCache)
        assert isinstance(a.cache.refresh_token, EmptyToken)
        assert isinstance(a.cache.access_token, EmptyToken)

    def test_api_pass_cache(self, set_env, sample_oid, sample_uri,
                            valid_access_token, valid_refresh_token):
        c = MemCache()

        c.refresh_token = valid_refresh_token
        c.access_token = valid_access_token

        assert valid_access_token.valid is True

        a = api(consumer_key=sample_oid, callback_url=sample_uri,
                store_tokens=False, cache=c)

        assert isinstance(a.cache, MemCache)
        assert a.cache.refresh_token == c.refresh_token
        assert a.cache.access_token == c.access_token

        assert a.cache.access_token.valid is True
