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

from pyTD.market.base import MarketData
from pyTD.utils import _handle_lists


class MarketHours(MarketData):
    """
    Class for retrieving data from the Get Market Hours endpoint.

    Parameters
    ----------
    markets : string, default "EQUITY", optional
        Desired market for retrieval (EQUITY, OPTION, FUTURE, BOND,
        or FOREX)
    date : datetime.datetime object, optional
        Data to retrieve hours for (defaults to current day)
    output_format: str, optional, default 'pandas'
        Desired output format (json or Pandas DataFrame).

        .. note:: JSON output formatting only if "FUTURE" is selected.
    api: pyTD.api.api object, optional
        A pyTD api object. If not passed, API requestor defaults to
        pyTD.api.default_api
    """
    _MARKETS = {"EQUITY": "EQ",
                "OPTION": "EQO",
                "FUTURE": None,
                "BOND": "BON",
                "FOREX": "forex"}

    def __init__(self, markets="EQUITY", date=None, output_format='pandas',
                 api=None):
        self.date = date or datetime.datetime.now()
        err_msg = "Please enter one more most markets (EQUITY, OPTION, etc.)"\
                  "for retrieval."
        self.markets = _handle_lists(markets, err_msg=err_msg)
        if not set(self.markets).issubset(self._MARKETS):
            raise ValueError("Please input valid markets for hours retrieval.")
        super(MarketHours, self).__init__(output_format, api)

    @property
    def params(self):
        return {
            "markets": ','.join(self.markets),
            "date": self.date.strftime('%Y-%m-%d')
        }

    @property
    def resource(self):
        return 'hours'

    def _convert_output(self, out):
        if "FUTURE" in self.markets:
            return out
        import pandas as pd
        markets = [sym.lower() for sym in self.markets]
        data = {market: out[market][self._MARKETS[market.upper()]] for market
                in markets}
        for market in markets:
            if market == "forex":
                hours = {"forex": data[market]}
            else:
                hours = data[market]["sessionHours"]
                hours = {k: hours[k][0] for k in hours}
            data[market] = pd.DataFrame(hours).sort_index(ascending=False)
        return data[markets[0]] if len(markets) == 1 else data