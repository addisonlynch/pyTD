.. _readme:


pyTD
====

.. image:: https://travis-ci.org/addisonlynch/pytd.svg?branch=master
    :target: https://travis-ci.org/addisonlynch/pytd

.. image:: https://codecov.io/gh/addisonlynch/pytd/branch/master/graphs/badge.svg?branch=master
    :target: https://codecov.io/gh/addisonlynch/pytd

.. image:: https://badge.fury.io/py/pytd.svg
    :target: https://badge.fury.io/py/pytd

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0

A robust Python Developer Kit to `TD Ameritrade for Developers
<https://developer.tdameritrade.com/>`__. Includes pre-defined classes and functions capable of obtaining market data and managing TD Ameritrade brokerage accounts.

Highlights:
-----------

* **Market Data:**

   * `Real\-Time Quotes <https://addisonlynch.github.io/pyTD/stable/market.html#quotes>`__
   * `Market Movers <https://addisonlynch.github.io/pyTD/stable/market.html#movers>`__
   * `Market Hours <https://addisonlynch.github.io/pyTD/stable/market.html#hours>`__
   * `Historical Prices <https://addisonlynch.github.io/pyTD/stable/market.html#historical-prices>`__
   * `Option Chains <https://addisonlynch.github.io/pyTD/stable/market.html#option-chains>`__
   * `Fundamentals <https://addisonlynch.github.io/pyTD/stable/>`__

* **Instrument Lookup**: Equities, ETFs, Mutual Funds, Futures, Forex, Indicies, Options, Bonds


**Coming Soon**

- **Accounts**: Balances, Positions, Watchlists, Statistics, Preferences
- **Trading**: Get/Place/Cancel/Replace Orders and Saved Orders

.. _readme.documentation:

Documentation
-------------

Full documentation is located at `addisonlynch.github.io/pyTD <https://addisonlynch.github.io/pyTD>`__.

.. _readme.installation:

Installation
------------

Dependencies
~~~~~~~~~~~~

- requests
- pandas


From PyPi with pip (latest stable release):

.. code-block:: shell

    $ pip install pyTD

From development repository (development version):

.. code-block:: shell

    $ git clone https://github.com/addisonlynch/pyTD
    $ cd pyTD
    $ python3 setup.py install

.. _readme.getting-started:

Getting Started
---------------

1. Register for a developer account at the `TD Ameritrade Developer Website
<https://developer.tdameritrade.com/>`__. A TD Ameritrade Developer account is
required to access TD Ameritrade Developer APIs. **This is separate from your
TD Ameritrade
Brokerage Account(s)**.

2. Create your TD Ameritrade Developer application.
See the pyTD
`documentation <https://addisonlynch.github.io/pytd/stable/faq.html#what-is-a-td-ameritrade-developer-account>`__
for more information on setting up an application.

3. Run ``pyTD.configure``
(`docs <configuration.html#the-all-in-one-solution-pytd-configure>`__ to set up
your `configuration
directory <https://addisonlynch.github.io/pytd/stable/configuration.html#configuration-directory>`__
and generate your self-signed SSL certificate and key. Note: if using MacOS,
you may not be able to generate the certificate and key using
``pyTD.configure``. See `Generating an SSL
Key/Certificate <https://addisonlynch.github.io/pytd/stable/configuration.html#generating-an-ssl-key-certificate>`__
for more information.

4. Authenticate and Authorize pyTD by simply calling any function which returns data. For example ``get_quotes`` from ``pyTD.market`` will automatically prompt you to obtain a new refresh token:

.. code-block:: python

    from pyTD.market import get_quotes

    get_quotes("AAPL")
    # WARNING:root:Need new refresh token.
    # Would you like to authorize a new refresh token? [y/n]:

Selecting ``y`` will open a browser for you to authorize your application. Once the browser opens, click "AUTHORIZE" to redirect to a TD Ameritrade login prompt.

From here, log in to your TD Ameritrade Brokerage Account. Once logged in, you have successfully authorized the application. The results of your query will display on screen.

After following the steps above, you will now have a new folder

.. _readme.configuration:

Configuration
-------------

Configuring pyTD can be done in one of three ways, depending on the production
environment. pyTD stores its configuration and caches refresh/access tokens by
default in the ~/.tdm directory (can be customized with the environment
variable ``TD_CONFIG_DIR``).

To configure pyTD and create the necessary directory structure,
enter your TD Ameritrade Developer app's Consumer Key (Consumer Key) and Callback URL (Callback URL) by one of the below methods:


**Environment Variables (Recommended):**

.. code-block:: shell

    $ export TD_CONSUMER_KEY=TEST@AMER.OAUTHAP
    $ export TD_CALLBACK_URL=https://localhost:8080


**Pass as argument:**

.. code-block:: python

    from pyTD import configure

    configure({
        "callback_url": "https://localhost:8080",
        "consumer_key": "TEST@AMER.OAUTHAP"
    })

*Note: this configuration will be cached in the current session only*

**Instantiate a non-global API object:**

.. code-block:: python

    from pyTD import api

    a = api({
        "callback_url": "https://localhost:8080",
        "consumer_key": "TEST@AMER.OAUTHAP"
    })

The Consumer Key and Callback URL passed in these scenarios will be cached in your configuration directory in the file tdm_config. Tokens will be cached in a file whose name is your Consumer Key.

.. _readme.market_data:

Market Data
-----------

.. _readme.quotes:

Quotes
~~~~~~

`Get real-time or delayed stock quotes <https://developer.tdameritrade.com/quotes/apis/get/marketdata/quotes>`__

.. code-block:: python

    from pyTD.market import get_quotes

    get_quotes("AAPL")

.. _readme.movers:

Movers
~~~~~~

`Get market movers, up or down, by change or percent <https://developer.tdameritrade.com/movers/apis/get/marketdata/%7Bindex%7D/movers>`__

.. code-block:: python

    from pyTD.market import get_movers

    get_movers("$DJI", direction='up', change='percent')

.. _readme.hours:

Hours
~~~~~

`Get operating hours of markets <https://developer.tdameritrade.com/market-hours/apis>`__

.. code-block:: python

    import datetime
    from pyTD.market import get_market_hours

    date = datetime.datetime(2018, 6, 29)

    get_market_hours("EQUITY", date=date)


.. _readme.option_chains:

Option Chains
~~~~~~~~~~~~~

`Get option chains for a optionable symbols <https://developer.tdameritrade.com/option-chains/apis>`__

.. code-block:: python

    from pyTD.market import get_option_chain

    get_option_chain("AAPL")

.. _readme.price_history:

Price History
~~~~~~~~~~~~~

`Get historical price data for charts <https://developer.tdameritrade.com/price-history/apis>`__

.. code-block:: python

    import datetime
    from pyTD.market import get_price_history

    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2018, 1, 1)

    get_price_history("AAPL", startDate=start, endDate=end)

.. _readme.fundamentals:

Fundamentals
~~~~~~~~~~~~

`Get fundamental data <https://developer.tdameritrade.com/instruments/apis/get/instruments>`__

.. code-block:: python

    from pyTD.market import get_fundamentals

    get_fundamentals("AAPL")

.. _readme.instruments:

Instruments
-----------

`Get Instrument by CUSIP ID <https://developer.tdameritrade.com/instruments/apis/get/instruments/%7Bcusip%7D>`__

.. code-block:: python

    from pyTD.instruments import get_instrument

    get_instrument("037833100")

`Get Instrument by symbol <https://developer.tdameritrade.com/instruments/apis/get/instruments/%7Bcusip%7D>`__

.. code-block:: python

    get_instrument("AAPL")


`Get Instrument by description <https://developer.tdameritrade.com/instruments/apis/get/instruments>`__

.. code-block:: python

    from pyTD.instruments import get_instruments

    get_instruments("computer", projection="desc-search")


`Get Instrument via regex <https://developer.tdameritrade.com/instruments/apis/get/instruments>`__

.. code-block:: python

    get_instruments("AAP.*", projection="symbol-regex")



.. _readme.logging:

Logging
-------

By default, logging to the console is disabled in pyTD, but can be set in a few different ways to either INFO, DEBUG, or ERROR

1. Environment variable:

.. code-block:: shell

        $ export TD_LOG_LEVEL=INFO

2. Setting ``pyTD.log_level``:

.. code-block:: python

        import pyTD
        pyTD.log_level = "INFO"

3. Using Python's `logging <https://docs.python.org/3/library/logging.html>`__ module:

.. code-block:: python

        import logging
        logging.basicConfig()
        logging.getLogger("pyTD").setLevel(logging.INFO)

.. _readme.python_versions:

Supported Python Versions
-------------------------

Python versions 2.7 and 3.4+ are supported by pyTD.


.. _readme.faq:

Frequently Asked Questions
--------------------------

- `How do I get my Consumer Key and Callback URL? <http://addisonlynch.github.io/pyTD/stable/faq.html#how-do-i-get-my-oauth-id-and-redirect-uri>`__
- `What is OAuth 2.0? <https://addisonlynch/github.io/stable/faq.html#what-is-oauth-2-0>`__
- `What should my Callback URL be? <https://addisonlynch/github.io/stable/faq.html#what-should-my-redirect-uri-be>`__
- `What is a CUSIP ID? <https://addisonlynch/github.io/stable/faq.html#what-is-a-cusip-id>`__
.. _readme.contact:

Contact
-------

Email: `ahlshop@gmail.com <ahlshop@gmail.com>`__

Twitter: `alynchfc <https://www.twitter.com/alynchfc>`__

.. _readme.license:

License
-------

Copyright © 2018 Addison Lynch

See LISCENSE for details

