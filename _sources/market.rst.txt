.. _market:


Market Data
===========

TD Ameritrade provides various endpoints to obtain Market Data for various instruments and markets across asset classes.

**Endpoints**

1. :ref:`Quotes <market.quotes>`
2. :ref:`Market Movers <market.movers>`
3. :ref:`Market Hours <market.hours>`
4. :ref:`Option Chains <market.option-chains>`
5. :ref:`Price History <market.price-history>`
6. :ref:`Fundamentals <market.fundamentals>`


.. _market.quotes:

Quotes
------

The `Get Quote
<https://developer.tdameritrade.com/quotes/apis/get/marketdata/%7Bsymbol%7D/quotes>`__
and `Get Quotes
<https://developer.tdameritrade.com/quotes/apis/get/marketdata/quotes>`__
endpoints provide real-time and delayed quotes. Access is provided by pyTD
through the top-level function ``get_quotes``, which combines functionality of
the two endpoints.


.. autofunction:: pyTD.market.get_quotes

.. _market.quotes-examples:

Examples
~~~~~~~~

**Single Stock**

.. ipython:: python

    from pyTD.market import get_quotes

    get_quotes("AAPL").head()


**Multiple Stocks**

.. ipython:: python

    get_quotes(["AAPL", "TSLA"]).head()



.. _market.movers:

Movers
------

The `Get Movers <https://developer.tdameritrade.com/movers/apis/get/marketdata/%7Bindex%7D/movers>`__ endpoint provides market movers (up or down) for a specified index. Access is provided by pyTD through the top-level function ``get_movers``.

**Format** - 'json' (dictionary) or 'pandas' (Pandas DataFrame)

.. autofunction:: pyTD.market.get_movers

.. note:: The desired index should be prefixed with ``$``. For instance, the Dow Jones Industrial Average is ``$DJI``.

.. warning:: This endpoint may return empty outside of Market Hours.

.. _market.movers-examples:

Examples
~~~~~~~~

.. ipython:: python

    from pyTD.market import get_movers

    get_movers("$DJI")


.. _market.hours:

Hours
-----

The `Get Market Hours
<https://developer.tdameritrade.com/market-hours/apis/get/marketdata/hours>`__
endpoint provides market hours for various markets, including equities,
options, and foreign exchange (forex). Access is provided by pyTD through the top-level function ``get_market_hours``.

By default, ``get_market_hours`` returns the market hours of the current date,
but can do so for any past or future date when passed the optional keyword argument ``date``.

.. autofunction :: pyTD.market.get_market_hours

.. _market.hours-examples:

Examples
~~~~~~~~

.. ipython:: python

    from pyTD.market import get_market_hours

    get_market_hours("EQUITY")


.. _market.option-chains:

Option Chains
-------------

The `Get Option Chains <https://developer.tdameritrade.com/option-chains/apis/get/marketdata/chains>`__ endpoint provides option chains for optionable equities symbols. Access is provided by pyTD through the top-level function ``get_option_chains``.

``get_option_chains`` accepts a variety of arguments, which allow filtering of the results by criteria such as strike price, moneyness, and expiration date, among others. Futher, it is possible to specify certain parameters to be used in calculations for analytical strategy chains.


.. autofunction :: pyTD.market.get_option_chains

.. _market.option-chains-examples:

Examples
~~~~~~~~

Simple
^^^^^^

.. ipython:: python

    from pyTD.market import get_option_chains

    get_option_chains("AAPL")

.. _market.price-history:

Historical Prices
-----------------

The `Get Price History <https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory>`__ endpoint provides historical pricing data for symbols across asset classes. Access is provided by pyTD through the top-level function ``get_price_history``.


.. autofunction :: pyTD.market.get_price_history

.. _market.price-history-examples:

Examples
~~~~~~~~

.. ipython:: python

    import datetime
    from pyTD.market import get_price_history

    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2018, 1, 1)

    get_price_history("AAPL", start_date=start, end_date=end).head()


.. _market.fundamentals:

Fundamental Data
----------------

Fundamental data can also be accesed through ``get_fundamentals``, which wraps
``pyTD.instruments.get_instruments`` for convenience.

.. ipython:: python

    from pyTD.market import get_fundamentals

    get_fundamentals("AAPL").head()
