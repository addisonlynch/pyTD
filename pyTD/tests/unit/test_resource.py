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


from pyTD.api import api
from pyTD.resource import Get
from pyTD.utils.exceptions import TDQueryError
from pyTD.utils.testing import MockResponse


@pytest.fixture(params=[
    MockResponse("", 200),
    MockResponse('{"error":"Not Found."}', 200)], ids=[
        "Empty string",
        '"Error" in response',
])
def bad_json(request):
    return request.param


class TestResource(object):

    def test_get_raises_json(self, bad_json, valid_cache,
                             sample_oid, sample_uri):
        a = api(consumer_key=sample_oid, callback_url=sample_uri,
                cache=valid_cache)
        a.request = lambda s, *a, **k: bad_json
        resource = Get(api=a)

        with pytest.raises(TDQueryError):
            resource.get()
