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

import logging

from pyTD import BASE_URL
from pyTD.api import default_api
from pyTD.utils.exceptions import TDQueryError

logger = logging.getLogger(__name__)


class Resource(object):
    """
    Base class for all REST services
    """
    _BASE_URL = BASE_URL

    def __init__(self, api=None):
        self.api = api or default_api()

    @property
    def url(self):
        return self._BASE_URL

    @property
    def params(self):
        return {}

    @property
    def data(self):
        return {}

    @property
    def headers(self):
        return {
            "content-type": "application/json"
        }


class Get(Resource):
    """
    GET requests
    """
    def get(self, url=None, params=None):
        params = params or self.params
        url = url or self.url

        response = self.api.request("GET", url=url, params=params)

        # Convert GET requests to JSON
        try:
            json_data = response.json()
        except ValueError:
            raise TDQueryError(message="An error occurred during the query.",
                               response=response)
        if "error" in json_data:
            raise TDQueryError(response=response)
        return json_data
