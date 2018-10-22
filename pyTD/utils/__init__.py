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
import requests
import datetime as dt

import pandas as pd
from pandas import to_datetime
import pandas.compat as compat

from pyTD.compat import is_number


logger = logging.getLogger(__name__)


def bprint(msg):
    return color.BOLD + msg + color.ENDC


class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRN = '\x1B[32m'
    RED = '\x1B[31m'


def gprint(msg):
    return(color.GRN + msg + color.ENDC)


def _handle_lists(l, mult=True, err_msg=None):
    if isinstance(l, (compat.string_types, int)):
        return [l] if mult is True else l
    elif isinstance(l, pd.DataFrame) and mult is True:
        return list(l.index)
    elif mult is True:
        return list(l)
    else:
        raise ValueError(err_msg or "Only 1 symbol/market parameter allowed.")


def _init_session(session):
    if session is None:
        session = requests.session()
    return session


def input_require(msg):
    result = ''
    while result == '':
        result = input(msg)
    return result


def rprint(msg):
    return(color.BOLD + color.RED + msg + color.ENDC)


def _sanitize_dates(start, end, set_defaults=True):
    """
    Return (datetime_start, datetime_end) tuple
    if start is None - default is 2017/01/01
    if end is None - default is today

    Borrowed from Pandas DataReader
    """
    if is_number(start):
        # regard int as year
        start = dt.datetime(start, 1, 1)
    start = to_datetime(start)

    if is_number(end):
        end = dt.datetime(end, 1, 1)
    end = to_datetime(end)

    if set_defaults is True:
        if start is None:
            start = dt.datetime(2017, 1, 1, 0, 0)
        if end is None:
            end = dt.datetime.today()
    if start and end:
        if start > end:
            raise ValueError('start must be an earlier date than end')
    return start, end


def to_timestamp(date):
    return int(date.strftime("%s"))


def yn_require(msg):
    template = "{} [y/n]: "
    result = ''
    YES = ["y", "Y", "Yes", "yes"]
    NO = ["n", "N", "No", "no"]
    while result not in YES and result not in NO:
        result = input_require(template.format(msg))
    if result in YES:
        return True
    if result in NO:
        return False
