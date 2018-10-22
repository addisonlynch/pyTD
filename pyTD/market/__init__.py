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

from pyTD.instruments.base import Instruments
from pyTD.market.hours import MarketHours
from pyTD.market.quotes import Quotes
from pyTD.market.movers import Movers
from pyTD.market.options import Options
from pyTD.market.price_history import PriceHistory


def get_fundamentals(*args, **kwargs):
    """
    Retrieve fundamental data for a diven symbol or CUSIP ID

    Parameters
    ----------
    symbol: str
        A CUSIP ID, symbol, regular expression, or snippet (depends on the
        value of the "projection" variable)
    output_format: str, default "pandas", optional
        Desired output format. "pandas" or "json"
    """
    kwargs.update({"projection": "fundamental"})
    return Instruments(*args, **kwargs).execute()


def get_quotes(*args, **kwargs):
    """
    Function for retrieving quotes from the Get Quotes endpoint.

    Parameters
    ----------
    symbols : str, array-like object (list, tuple, Series), or DataFrame
        Single stock symbol (ticker), array-like object of symbols or
        DataFrame with index containing up to 100 stock symbols.
    output_format: str, default 'pandas', optional
        Desired output format (json or DataFrame)
    kwargs: additional request parameters (see _TDBase class)
    """
    return Quotes(*args, **kwargs).execute()


def get_market_hours(*args, **kwargs):
    """
    Function to retrieve market hours for a given market from the Market
    Hours endpoint

    Parameters
    ----------
    market: str, default EQUITY, optional
        The market to retrieve operating hours for
    date : string or DateTime object, (defaults to today's date)
        Operating date, timestamp. Parses many different kind of date
        representations (e.g., 'JAN-01-2015', '1/1/15', 'Jan, 1, 1980')
    output_format: str, default 'pandas', optional
        Desired output format (json or DataFrame)
    kwargs: additional request parameters (see _TDBase class)
    """
    return MarketHours(*args, **kwargs).execute()


def get_movers(*args, **kwargs):
    """
    Function for retrieving market moveers from the Movers endpoint

    Parameters
    ----------
    index: str
        The index symbol to get movers from
    direction: str, default up, optional
        Return up or down movers
    change: str, default percent, optional
        Return movers by percent change or value change
    output_format: str, default 'pandas', optional
        Desired output format (json or DataFrame)
    kwargs: additional request parameters (see _TDBase class)
    """
    return Movers(*args, **kwargs).execute()


def get_option_chains(*args, **kwargs):
    """
    Function to retrieve option chains for a given symbol from the Option
    Chains endpoint

    Parameters
    ----------

    contractType: str, default ALL, optional
        Desired contract type (CALL, PUT, ALL)
    strikeCount: int, optional
        Number of strikes to return above and below the at-the-money price
    includeQuotes: bool, default False, optional
        Include quotes for options in the option chain
    strategy: str, default None, optional
        Passing a value returns a strategy chain (SINGLE or ANALYTICAL)
    interval: int, optional
        Strike interval for spread strategy chains
    strike: float, optional
        Filter options that only have a certain strike price
    range: str, optional
        Returns options for a given range (ITM, OTM, etc.)
    fromDate: str or datetime.datetime object, optional
        Only return options after this date
    toDate: str or datetime.datetime object, optional
        Only return options before this date
    volatility: float, optional
        Volatility to use in calculations (for analytical strategy chains)
    underlyingPrice: float, optional
        Underlying price to use in calculations (for analytical strategy
        chains)
    interestRate: float, optional
        Interest rate to use in calculations (for analytical strategy
        chains)
    daysToExpiration: int, optional
        Days to expiration to use in calulations (for analytical
        strategy chains)
    expMonth: str, optional
        Expiration month (format JAN, FEB, etc.) to use in calculations
        (for analytical strategy chains), default ALL
    optionType: str, optional
        Type of contracts to return (S: standard, NS: nonstandard,
        ALL: all contracts)
    output_format: str, optional, default 'pandas'
        Desired output format
    api: pyTD.api.api object, optional
        A pyTD api object. If not passed, API requestor defaults to
        pyTD.api.default_api
    kwargs: additional request parameters (see _TDBase class)
    """
    return Options(*args, **kwargs).execute()


def get_price_history(*args, **kwargs):
    """
    Function to retrieve price history for a given symbol over a given period

    Parameters
    ----------
    symbols : string, array-like object (list, tuple, Series), or DataFrame
        Desired symbols for retrieval
    periodType: str, default DAY, optional
        The type of period to show
    period: int, optional
        The number of periods to show
    frequencyType: str, optional
        The type of frequency with which a new candle is formed
    frequency: int, optional
        The number of frequencyType to includ with each candle
    startDate : string or DateTime object, optional
        Starting date, timestamp. Parses many different kind of date
        representations (e.g., 'JAN-01-2015', '1/1/15', 'Jan, 1, 1980')
    endDate : string or DateTime object, optional
        Ending date, timestamp. Parses many different kind of date
        representations (e.g., 'JAN-01-2015', '1/1/15', 'Jan, 1, 1980')
    extended: str or bool, default 'True'/True, optional
        True to return extended hours data, False for regular hours only
    output_format: str, default 'pandas', optional
        Desired output format (json or DataFrame)
    """
    return PriceHistory(*args, **kwargs).execute()


# def get_history_intraday(symbols, start, end, interval='1m', extended=True,
#                          output_format='pandas'):
#     """
#     Function to retrieve intraday price history for a given symbol

#     Parameters
#     ----------
#     symbols : string, array-like object (list, tuple, Series), or DataFrame
#         Desired symbols for retrieval
#     startDate : string or DateTime object, optional
#         Starting date, timestamp. Parses many different kind of date
#         representations (e.g., 'JAN-01-2015', '1/1/15', 'Jan, 1, 1980')
#     endDate : string or DateTime object, optional
#         Ending date, timestamp. Parses many different kind of date
#         representations (e.g., 'JAN-01-2015', '1/1/15', 'Jan, 1, 1980')
#     interval: string, default '1m', optional
#         Desired interval (1m, 5m, 15m, 30m, 60m)
#     needExtendedHoursData: str or bool, default 'True'/True, optional
#         True to return extended hours data, False for regular hours only
#     output_format: str, default 'pandas', optional
#         Desired output format (json or DataFrame)
#     """
#     result = PriceHistory(symbols, start_date=start, end_date=end,
#                           extended=extended,
#                           output_format=output_format).execute()
#     if interval == '1m':
#         return result
#     elif interval == '5m':
#         sample = result.index.floor('5T').drop_duplicates()
#         return result.reindex(sample, method='ffill')
#     elif interval == '15m':
#         sample = result.index.floor('15T').drop_duplicates()
#         return result.reindex(sample, method='ffill')
#     elif interval == '30m':
#         sample = result.index.floor('30T').drop_duplicates()
#         return result.reindex(sample, method='ffill')
#     elif interval == '60m':
#         sample = result.index.floor('60T').drop_duplicates()
#         return result.reindex(sample, method='ffill')
#     else:
#         raise ValueError("Interval must be 1m, 5m, 15m, 30m, or 60m.")


# def get_history_daily(symbols, start, end, output_format='pandas'):
#     return PriceHistory(symbols, start_date=start, end_date=end,
#                         frequency_type='daily',
#                         output_format=output_format).execute()
