.. _instruments:

.. ipython:: python
    :suppress:
    import requests_cache
    from pyTD.api import api
    requests_cache.install_cache("cache/pyTD")

    __api__ = api(consumer_key="TEST@AMER.OAUTHAP",
                  callback_url="https://localhost:8080",
                  session=requests_cache.CachedSession(),
                  store_tokens=False)

Instruments
===========

The `Instruments <https://developer.tdameritrade.com/instruments/apis>`__
endpoints allow for retrieval of instrument and fundamental
data. These endpoints are `Search Instruments
<https://developer.tdameritrade.com/instruments/apis/get/instruments>`__ and
`Get Instrument
<https://developer.tdameritrade.com/instruments/apis/get/instruments/%7Bcusip%7D>`__.

.. _instruments.get-instrument

Get Instrument
--------------

pyTD provides access to Get Instruments through the ``get_instrument``
function. Simply enter a symbol:

.. ipython:: python

    from pyTD.instruments import get_instrument

    get_instrument("AAPL")

or a CUSIP ID:

.. ipython:: python

    get_instrument("68389X105")

.. _instruments.search-instruments:

Search Instruments
------------------

Search Instruments is implemented through ``get_instruments``.

``projection``
~~~~~~~~~~~~~~

There are five types of searches which can be performed:

1. ``symbol-search`` (default): Retrieve instrument data of a specific symbol
or CUSIP
(similar to ``get_instrument``)

.. ipython:: python

    from pyTD.instruments import get_instruments

    get_instruments("AAPL")


2. ``symbol-regex``: Retrieve instrument data for all symbols matching regex.
Example: ``symbol=XYZ.*`` will return all symbols beginning with XYZ

.. ipython:: python

    get_instruments("AAP.*", projection="symbol-regex")


3. ``desc-search``: Retrieve instrument data for instruments whose description
contains the word supplied. Example: ``symbol=FakeCompany`` will return all
instruments with FakeCompany in the description.

.. ipython:: python

    get_instruments("computer", projection="desc-search")


4. ``desc-regex``: Search description with full regex support. Example:
``symbol=XYZ.[A-C]`` returns all instruments whose descriptions contain a word
beginning with XYZ followed by a character A through C.

.. ipython:: python

    get_instruments("COM.*", projection="desc-regex")


5. ``fundamental``: Returns fundamental data for a single instrument specified by exact symbol.

.. ipython:: python

    get_instruments("AAPL", projection="fundamental").head()
