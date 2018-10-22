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
import pytest
import pandas as pd

from pyTD.utils import _handle_lists, _sanitize_dates


@pytest.fixture(params=[
    1,
    "test"
], ids=[
    "int",
    "string"
])
def single(request):
    return request.param


@pytest.fixture(params=[
    [1, 2, 3],
    (1, 2, 3),
    pd.DataFrame([], index=[1, 2, 3]),
    pd.Series([1, 2, 3]),
], ids=[
    "list",
    "tuple",
    "DataFrame",
    "Series"
])
def mult(request):
    return request.param


class TestUtils(object):

    def test_handle_lists_sing(self, single):
        assert _handle_lists(single, mult=False) == single
        assert _handle_lists(single) == [single]

    def test_handle_lists_mult(self, mult):
        assert _handle_lists(mult) == [1, 2, 3]

    def test_handle_lists_err(self, mult):
        with pytest.raises(ValueError):
            _handle_lists(mult, mult=False)

    def test_sanitize_dates_years(self):
        expected = (datetime.datetime(2017, 1, 1),
                    datetime.datetime(2018, 1, 1))
        assert _sanitize_dates(2017, 2018) == expected

    def test_sanitize_dates_default(self):
        exp_start = datetime.datetime(2017, 1, 1, 0, 0)
        exp_end = datetime.datetime.today()
        start, end = _sanitize_dates(None, None)

        assert start == exp_start
        assert end.date() == exp_end.date()

    def test_sanitize_dates(self):
        start = datetime.datetime(2017, 3, 4)
        end = datetime.datetime(2018, 3, 9)

        assert _sanitize_dates(start, end) == (start, end)

    def test_sanitize_dates_error(self):
        start = datetime.datetime(2018, 1, 1)
        end = datetime.datetime(2017, 1, 1)

        with pytest.raises(ValueError):
            _sanitize_dates(start, end)
