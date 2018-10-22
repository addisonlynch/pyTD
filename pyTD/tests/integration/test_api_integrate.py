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

from pyTD.instruments import get_instrument
from pyTD.market import get_quotes
from pyTD.api import api

from pyTD.utils.testing import MockResponse


class TestMarketAPI(object):

    def test_quote_arg_api(self, valid_cache, sample_oid, sample_uri):
        a = api(consumer_key=sample_oid, callback_url=sample_uri,
                cache=valid_cache)
        r = MockResponse('{"symbol":"AAPL","quote":155.34}', 200)

        a.request = lambda s, *a, **k: r

        q = get_quotes("AAPL", api=a, output_format='json')

        assert isinstance(q, dict)
        assert q["symbol"] == "AAPL"

    def test_instrument_arg_api(self, valid_cache, sample_oid, sample_uri):
        a = api(consumer_key=sample_oid, callback_url=sample_uri,
                cache=valid_cache)

        r = MockResponse('{"symbol":"ORCL"}', 200)

        a.request = lambda s, *a, **k: r

        i = get_instrument("68389X105", api=a, output_format='json')

        assert isinstance(i, dict)
        assert i["symbol"] == "ORCL"
