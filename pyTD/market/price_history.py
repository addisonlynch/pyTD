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
import pandas as pd

from pyTD.auth import auth_check
from pyTD.market.base import MarketData
from pyTD.utils import _sanitize_dates, to_timestamp, _handle_lists
from pyTD.utils.exceptions import ResourceNotFound


class PriceHistory(MarketData):
    """
    Class for retrieving data from the Get Price History endpoint. Defaults to
    a 10-day, 1-minute chart

    Parameters
    ----------
    symbols : string, array-like object (list, tuple, Series), or DataFrame
        Desired symbols for retrieval
    period_type: str, default "day", optional
        Type of period to show (valid values are day, month, year, or ytd)
    period: int, optional
        The number of periods to show
    frequency_type: str, optional
        The type of frequency with which a new candle is formed. (valid values
        are minute, daily, weekly, monthly, depending on period type)
    frequency: int, default 1, optional
        The number of the frequency type to be included in each candle
    startDate : string or DateTime object, optional
        Starting date, timestamp. Parses many different kind of date. Defaults
        to 1/1/2018
        representations (e.g., 'JAN-01-2015', '1/1/15', 'Jan, 1, 1980')
    endDate : string or DateTime object, optional
        Ending date, timestamp. Parses many different kind of date
        representations (e.g., 'JAN-01-2015', '1/1/15', 'Jan, 1, 1980').
        Defaults to current day
    extended: bool, default True, optional
        True to return extended hours data, False for regular market hours only
    output_format: str, optional, default 'pandas'
        Desired output format (json or Pandas DataFrame)
    api: pyTD.api.api object, optional
        A pyTD api object. If not passed, API requestor defaults to
        pyTD.api.default_api
    """

    def __init__(self, symbols, **kwargs):
        self.period_type = kwargs.pop("period_type", "month")
        self.period = kwargs.pop("period", "")
        self.frequency_type = kwargs.pop("frequency_type", "daily")
        self.frequency = kwargs.pop("frequency", "")
        start = kwargs.pop("start_date", datetime.datetime(2018, 1, 1))
        end = kwargs.pop("end_date", datetime.datetime.today())
        self.need_extended = kwargs.pop("extended", "")
        self.output_format = kwargs.pop("output_format", 'pandas')
        self.opt = kwargs
        api = kwargs.get("api")
        self.start, self.end = _sanitize_dates(start, end, set_defaults=False)
        if self.start and self.end:
            self.start = to_timestamp(self.start) * 1000
            self.end = to_timestamp(self.end) * 1000
        self.symbols = _handle_lists(symbols)
        super(PriceHistory, self).__init__(self.output_format, api)

    @property
    def params(self):
        p = {
            "periodType": self.period_type,
            "period": self.period,
            "frequencyType": self.frequency_type,
            "frequency": self.frequency,
            "startDate": self.start,
            "endDate": self.end,
            "needExtendedHoursData": self.need_extended
            }
        return p

    @property
    def resource(self):
        return 'pricehistory'

    @property
    def url(self):
        return "%s%s/{}/%s" % (self._BASE_URL, self.endpoint, self.resource)

    def _convert_output(self, out):
        for sym in self.symbols:
            out[sym] = self._convert_output_one(out[sym])
        return pd.concat(out.values(), keys=out.keys(), axis=1)

    def _convert_output_one(self, out):
        df = pd.DataFrame(out)
        df = df.set_index(pd.DatetimeIndex(df["datetime"]/1000*10**9))
        df = df.drop("datetime", axis=1)
        return df

    @auth_check
    def execute(self):
        result = {}
        for sym in self.symbols:
            data = self.get(url=self.url.format(sym))["candles"]
            FMT = "Price history for {} could not be retrieved"
            if not data:
                raise ResourceNotFound(message=FMT.format(sym))
            result[sym] = data
        if len(self.symbols) == 1:
            return self._output_format_one(result)
        else:
            return self._output_format(result)

    def _output_format_one(self, out):
        out = out[self.symbols[0]]
        if self.output_format == 'json':
            return out
        elif self.output_format == 'pandas':
            return self._convert_output_one(out)
        else:
            raise ValueError("Please enter a valid output format.")
