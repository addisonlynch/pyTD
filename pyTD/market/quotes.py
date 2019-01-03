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

from pyTD.auth import auth_check
from pyTD.market.base import MarketData
from pyTD.utils import _handle_lists
from pyTD.utils.exceptions import ResourceNotFound


class Quotes(MarketData):
    """
    Class for retrieving data from the Get Quote and Get Quotes endpoints.

    Parameters
    ----------
    symbols : string, array-like object (list, tuple, Series), or DataFrame
        Desired symbols for retrieval
    output_format: str, optional, default 'pandas'
        Desired output format (json or Pandas DataFrame)
    api: pyTD.api.api object, optional
        A pyTD api object. If not passed, API requestor defaults to
        pyTD.api.default_api
    """
    def __init__(self, symbols, output_format='pandas', api=None):
        self.symbols = _handle_lists(symbols)
        if len(self.symbols) > 100:
            raise ValueError("Please input a valid symbol or list of up to "
                             "100 symbols")
        super(Quotes, self).__init__(output_format, api)

    @property
    def resource(self):
        return "quotes"

    @property
    def params(self):
        return {
            "symbol": ','.join(self.symbols)
        }

    @auth_check
    def execute(self):
        data = self.get()
        if not data:
            raise ResourceNotFound(data, message="Quote for symbol %s not "
                                   "found." % self.symbols)
        else:
            return self._output_format(data)
