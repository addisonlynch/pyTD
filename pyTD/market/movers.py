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

from pyTD.market.base import MarketData
from pyTD.utils import _handle_lists


class Movers(MarketData):
    """
    Class for retrieving data from the Get Market Hours endpoint.

    Parameters
    ----------
    markets : str
        Ticker of market for retrieval
    direction : str, default 'up', optional
        To return movers with the specified directions of up or down
    change: str, default 'percent', optional
        To return movers with the specified change types of percent or value
    output_format: str, optional, default 'json'
        Desired output format (json or Pandas DataFrame)
    api: pyTD.api.api object, optional
        A pyTD api object. If not passed, API requestor defaults to
        pyTD.api.default_api

    WARNING: this endpoint is often not functional outside of trading hours.
    """

    def __init__(self, symbols, direction='up', change='percent',
                 output_format='pandas', api=None):
        self.direction = direction
        self.change = change
        err_msg = "Please input a valid market ticker (ex. $DJI)."
        self.symbols = _handle_lists(symbols, mult=False, err_msg=err_msg)
        super(Movers, self).__init__(output_format, api)

    def _convert_output(self, out):
        import pandas as pd
        return pd.DataFrame(out).set_index("symbol")

    @property
    def params(self):
        return {
            'change': self.change,
            'direction': self.direction
        }

    @property
    def resource(self):
        return "movers"

    @property
    def url(self):
        return "%s%s/%s/%s" % (self._BASE_URL, self.endpoint, self.symbols,
                               self.resource)
