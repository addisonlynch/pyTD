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
import pytest

from pyTD.tests.test_helper import pyTD

TDQueryError = pyTD.utils.exceptions.TDQueryError
ResourceNotFound = pyTD.utils.exceptions.ResourceNotFound


@pytest.fixture(scope='session', autouse=True)
def now():
    return datetime.datetime.now()


@pytest.mark.webtest
class TestMarketExceptions(object):

    def test_get_quotes_bad_symbol(self):
        with pytest.raises(TypeError):
            pyTD.market.get_quotes()

    def test_get_movers_bad_index(self):
        with pytest.raises(TypeError):
            pyTD.market.get_movers()

        with pytest.raises(TDQueryError):
            pyTD.market.get_movers("DJI")


@pytest.mark.webtest
class TestQuotes(object):

    def test_quotes_json_single(self):
        aapl = pyTD.market.get_quotes("AAPL", output_format='json')
        assert isinstance(aapl, dict)
        assert "AAPL" in aapl

    def test_quotes_json_multiple(self):
        aapl = pyTD.market.get_quotes(["AAPL", "TSLA"],
                                      output_format='json')
        assert isinstance(aapl, dict)
        assert len(aapl) == 2
        assert "TSLA" in aapl

    def test_quotes_pandas(self):
        df = pyTD.market.get_quotes("AAPL")
        assert isinstance(df, pd.DataFrame)
        assert "AAPL" in df

        assert len(df) == 41

    def test_quotes_bad_symbol(self):
        with pytest.raises(ResourceNotFound):
            pyTD.market.get_quotes("BADSYMBOL")

    def test_quotes_bad_params(self):
        bad = ["AAPL"] * 1000
        with pytest.raises(ValueError):
            pyTD.market.get_quotes(bad)


@pytest.mark.webtest
class TestMarketMovers(object):

    @pytest.mark.xfail(reason="Movers may return empty outside of "
                              "trading hours.")
    def test_movers_json(self):
        data = pyTD.market.get_movers("$DJI", output_format='json')
        assert isinstance(data, list)
        assert len(data) == 10

    @pytest.mark.xfail(reason="Movers may return empty outside of "
                              "trading hours.")
    def test_movers_pandas(self):
        data = pyTD.market.get_movers("$DJI")
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 10

    def test_movers_bad_index(self):
        with pytest.raises(ResourceNotFound):
            pyTD.market.get_movers("DJI")

    def test_movers_no_params(self):
        with pytest.raises(TypeError):
            pyTD.market.get_movers()


@pytest.mark.webtest
class TestMarketHours(object):

    def test_hours_bad_market(self):
        with pytest.raises(ValueError):
            pyTD.market.get_market_hours("BADMARKET")

        with pytest.raises(ValueError):
            pyTD.market.get_market_hours(["BADMARKET", "EQUITY"])

    def test_hours_default(self):
        data = pyTD.market.get_market_hours()

        assert len(data) == 8
        assert data.index[0] == "category"

    def test_hours_json(self):
        date = now()
        data = pyTD.market.get_market_hours("EQUITY", date,
                                            output_format='json')
        assert isinstance(data, dict)

    def test_hours_pandas(self):
        date = now()
        data = pyTD.market.get_market_hours("EQUITY", date)
        assert isinstance(data, pd.DataFrame)
        assert data.index[0] == "category"

    def test_hours_batch(self):
        data = pyTD.market.get_market_hours(["EQUITY", "OPTION"])

        assert len(data) == 8
        assert isinstance(data["equity"], pd.Series)


@pytest.mark.webtest
class TestOptionChains(object):

    def test_option_chain_no_symbol(self):
        with pytest.raises(TypeError):
            pyTD.market.get_option_chains()

    def test_option_chain_bad_symbol(self):
        with pytest.raises(ResourceNotFound):
            pyTD.market.get_option_chains("BADSYMBOL")

    def test_option_chain(self):
        data = pyTD.market.get_option_chains("AAPL", output_format='json')

        assert isinstance(data, dict)
        assert len(data) == 13
        assert data["status"] == "SUCCESS"

    def test_option_chain_call(self):
        data = pyTD.market.get_option_chains("AAPL", contract_type="CALL",
                                             output_format='json')

        assert not data["putExpDateMap"]

    def test_option_chain_put(self):
        data = pyTD.market.get_option_chains("AAPL", contract_type="PUT",
                                             output_format='json')

        assert not data["callExpDateMap"]


@pytest.mark.webtest
class TestPriceHistory(object):

    def test_price_history_no_symbol(self):
        with pytest.raises(TypeError):
            pyTD.market.get_price_history()

    def test_price_history_default_dates(self):
        data = pyTD.market.get_price_history("AAPL", output_format='json')

        assert isinstance(data, list)

    def test_price_history_bad_symbol(self):
        with pytest.raises(ResourceNotFound):
            pyTD.market.get_price_history("BADSYMBOL")

    def test_price_history_bad_symbols(self):
        with pytest.raises(ResourceNotFound):
            pyTD.market.get_price_history(["BADSYMBOL", "BADSYMBOL"],
                                          output_format='pandas')

    def test_price_history_json(self):
        data = pyTD.market.get_price_history("AAPL", output_format='json')

        assert isinstance(data, list)
        assert data[0]["close"] == 172.26
        assert data[0]["volume"] == 25555934
        assert len(data) > 100

    def test_batch_history_json(self):
        syms = ["AAPL", "TSLA", "MSFT"]
        data = pyTD.market.get_price_history(syms, output_format='json')

        assert len(data) == 3
        assert set(data) == set(syms)

    def test_price_history_pandas(self):
        data = pyTD.market.get_price_history("AAPL")

        assert isinstance(data, pd.DataFrame)

    def test_batch_history_pandas(self):
        data = pyTD.market.get_price_history(["AAPL", "TSLA", "MSFT"],
                                             output_format='pandas')

        assert isinstance(data, pd.DataFrame)
        assert isinstance(data.columns, pd.MultiIndex)

        assert "AAPL" in data.columns
        assert "TSLA" in data.columns
        assert "MSFT" in data.columns

        assert data.iloc[0].name.date() == datetime.date(2018, 1, 2)

    @pytest.mark.xfail(reason="Odd behavior on travis: wrong dates returned")
    def test_history_dates(self):
        start = datetime.date(2018, 1, 24)
        end = datetime.date(2018, 2, 12)

        data = pyTD.market.get_price_history("AAPL", start_date=start,
                                             end_date=end,
                                             output_format='pandas')

        assert data.iloc[0].name.date() == start
        assert data.iloc[-1].name.date() == datetime.date(2018, 2, 9)

        assert pd.infer_freq(data.index) == "B"


@pytest.mark.webtest
class TestFundamentals(object):

    def test_fundamentals(self):
        data = pyTD.market.get_fundamentals("AAPL")

        assert isinstance(data, pd.DataFrame)
        assert len(data) == 46
