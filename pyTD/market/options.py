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
from pyTD.utils.exceptions import ResourceNotFound


class Options(MarketData):
    """
    Class for retrieving data from the Get Option Chain endpoint

    Parameters
    ----------
    symbol: str
        Desired ticker for retrieval
    contract_type: str, default "ALL", optional
        Type of contracts to return in the chain. Can be CALL,
        PUT, or ALL
    strike_count: int, optional
        The number of strikes to return above and below the
        at-the-money price
    include_quotes: bool, optional
        Include quotes for options in the option chain
    strategy: str, default "SINGLE", optional
        Passing a value returns a Strategy Chain. Possible values are SINGLE,
        ANALYTICAL, COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE,
        BUTTERFLY, CONDOR, DIAGONAL, COLLAR, ROLL
    interval: int, optional
        Strike interval for spread strategy chains
    strike: float, optional
        Strike price to return options only at that strike price
    range: str, default "ALL", optional
        Returns options for the given range. Possible values are ITM, NTM,
        OTM, SAK, SBK, SNK, ALL
    from_date : datetime.datetime object, optional
        Only return expirations after this date
    to_date: datetime.datetime object, optional
        Only return expirations before this date
    volatility: int or float, optional
        Volatility to use in calculations
    underlying_price: int or float, optional
        Underlying price to use in calculations
    interest_rate: int or float, optional
        Interest rate to use in calculations
    days_to_expiration: int, optional
        Days to expiration to use in calculations
    exp_month: str, default "ALL", optional
        Return only options expiring in the specified month. Month is given in
        3-character format (JAN, FEB, MAR, etc.)
    option_type: str, default "ALL", optional
        Type of contracts to return (S, NS, ALL)
    output_format: str, optional, default 'json'
        Desired output format
    api: pyTD.api.api object, optional
        A pyTD api object. If not passed, API requestor defaults to
        pyTD.api.default_api
    """

    def __init__(self, symbol, **kwargs):
        self.contract_type = kwargs.pop("contract_type", "ALL")
        self.strike_count = kwargs.pop("strike_count", "")
        self.include_quotes = kwargs.pop("include_quotes", "")
        self.strategy = kwargs.pop("strategy", "")
        self.interval = kwargs.pop("interval", "")
        self.strike = kwargs.pop("strike", "")
        self.range = kwargs.pop("range", "")
        self.from_date = kwargs.pop("from_date", "")
        self.to_date = kwargs.pop("to_date", "")
        self.volatility = kwargs.pop("volatility", "")
        self.underlying_price = kwargs.pop("underlying_price", "")
        self.interest_rate = kwargs.pop("interest_rate", "")
        self.days_to_expiration = kwargs.pop("days_to_expiration", "")
        self.exp_month = kwargs.pop("exp_month", "")
        self.option_type = kwargs.pop("option_type", "")
        self.output_format = kwargs.pop("output_format", 'pandas')
        self.api = kwargs.pop("api", None)
        self.opts = kwargs
        self.symbols = _handle_lists(symbol)
        super(Options, self).__init__(self.output_format, self.api)

    @property
    def params(self):
        p = {
            "symbol": self.symbols,
            "contractType": self.contract_type,
            "strikeCount": self.strike_count,
            "includeQuotes": self.include_quotes,
            "strategy": self.strategy,
            "interval": self.interval,
            "strike": self.strike,
            "range": self.range,
            "fromDate": self.from_date,
            "toDate": self.to_date,
            "volatility": self.volatility,
            "underlyingPrice": self.underlying_price,
            "interestRate": self.interest_rate,
            "daysToExpiration": self.days_to_expiration,
            "expMonth": self.exp_month,
            "optionType": self.option_type
        }
        p.update(self.opts)
        return p

    @property
    def resource(self):
        return 'chains'

    def _convert_output(self, out):
        import pandas as pd
        ret = {}
        ret2 = {}
        if self.contract_type in ["CALL", "ALL"]:
            for date in out['callExpDateMap']:
                for strike in out['callExpDateMap'][date]:
                    ret[date] = (out['callExpDateMap'][date][strike])[0]
        if self.contract_type in ["PUT", "ALL"]:
            for date in out['putExpDateMap']:
                for strike in out['putExpDateMap'][date]:
                    ret2[date] = (out['putExpDateMap'][date][strike])[0]
        return pd.concat([pd.DataFrame(ret).T, pd.DataFrame(ret2).T], axis=1,
                         keys=["calls", "puts"])

    def get(self):
        data = super(Options, self).get()
        if data["status"] == "FAILED":
            raise ResourceNotFound(message="Option chains for %s not "
                                   "found." % self.symbols)
        return data
