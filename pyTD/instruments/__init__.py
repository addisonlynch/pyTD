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


def get_instrument(*args, **kwargs):
    """
    Retrieve instrument from CUSIP ID from the Get Instrument endpoint

    Parameters
    ----------
    symbol: str
        A CUSIP ID or symbol
    output_format: str, default "pandas", optional
        Desired output format. "pandas" or "json"
    """
    return Instruments(*args, **kwargs).execute()


def get_instruments(*args, **kwargs):
    """
    Search or retrieve instrument data, including fundamental data

    Parameters
    ----------
    symbol: str
        A CUSIP ID, symbol, regular expression, or snippet (depends on the
        value of the "projection" variable)
    projection: str, default symbol-search, optional
        Type of request (see documentation)
    output_format: str, default "pandas", optional
        Desired output format. "pandas" or "json"
    """
    return Instruments(*args, **kwargs).execute()
