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

import pandas as pd
import pytest

from pyTD.tests.test_helper import pyTD

ResourceNotFound = pyTD.utils.exceptions.ResourceNotFound
TDQueryError = pyTD.utils.exceptions.TDQueryError


@pytest.mark.webtest
class TestInstrument(object):

    def test_instrument_no_symbol(self):
        with pytest.raises(TypeError):
            pyTD.instruments.get_instrument()

    def test_instrument_bad_instrument(self):
        with pytest.raises(ResourceNotFound):
            pyTD.instruments.get_instrument("BADINSTRUMENT")

    def test_instrument_cusip(self):
        cusip = "68389X105"
        data = pyTD.instruments.get_instrument(cusip,
                                               output_format='json')[cusip]

        assert isinstance(data, dict)

        assert data["symbol"] == "ORCL"
        assert data["exchange"] == "NYSE"

    def test_instruments_cusip(self):
        cusip = "17275R102"
        data = pyTD.instruments.get_instruments(cusip,
                                                output_format='json')[cusip]

        assert isinstance(data, dict)

        assert data["symbol"] == "CSCO"
        assert data["exchange"] == "NASDAQ"

    def test_instrument_cusp_pandas(self):
        data = pyTD.instruments.get_instrument("68389X105").T

        assert isinstance(data, pd.DataFrame)

        assert len(data) == 1
        assert len(data.columns) == 5
        assert data.iloc[0]["symbol"] == "ORCL"

    def test_instrument_symbol(self):
        data = pyTD.instruments.get_instrument("AAPL").T

        assert isinstance(data, pd.DataFrame)

        assert len(data) == 1
        assert len(data.columns) == 5
        assert data.iloc[0]["symbol"] == "AAPL"

    def test_instruments_fundamental(self):
        data = pyTD.instruments.get_instruments("AAPL",
                                                projection="fundamental").T

        assert isinstance(data, pd.DataFrame)

        assert len(data.columns) == 46
        assert data.iloc[0]["symbol"] == "AAPL"

    def test_instruments_regex(self):
        data = pyTD.instruments.get_instruments("AAP.*",
                                                projection="symbol-regex").T

        assert isinstance(data, pd.DataFrame)

        assert data.shape == (13, 5)

    def test_instruments_bad_projection(self):
        with pytest.raises(TDQueryError):
            pyTD.instruments.get_instruments("AAPL",
                                             projection="BADPROJECTION")
