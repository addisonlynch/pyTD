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

from pyTD.auth import auth_check
from pyTD.base import _pyTD_base

logger = logging.getLogger(__name__)


class MarketData(_pyTD_base):
    """
    Base class for retrieving market-based information. This includes the
    following endpoint groups:
        - Market Hours
        - Movers
        - Option Chains
        - Price History
        - Quotes

    Parameters
    ----------
    symbols: str or list-like, optional
        A symbol or list of symbols
    output_format: str, optional, default 'json'
        Desired output format (json or Pandas DataFrame)
    api: pyTD.api.api object, optional
        A pyTD api object. If not passed, API requestor defaults to
        pyTD.api.default_api
    """

    def __init__(self, output_format='pandas', api=None):
        self.output_format = output_format
        super(MarketData, self).__init__(api=api)

    @property
    def endpoint(self):
        return "marketdata"

    @property
    def resource(self):
        raise NotImplementedError

    @property
    def url(self):
        return "%s%s/%s" % (self._BASE_URL, self.endpoint, self.resource)

    def _convert_output(self, out):
        import pandas as pd
        return pd.DataFrame(out)

    @auth_check
    def execute(self):
        out = self.api.get(url=self.url, params=self.params)
        return self._output_format(out)

    def _output_format(self, out):
        if self.output_format == 'json':
            return out
        elif self.output_format == 'pandas':
            return self._convert_output(out)
        else:
            raise ValueError("Please enter a valid output format.")
