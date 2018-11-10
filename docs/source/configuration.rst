.. _config:


Configuration
=============


- :ref:`config.environment`
- :ref:`config.user_agent`
- :ref:`config.logging`
- :ref:`config.appendix`


The following are the available configuration options for pyTD.


**Environment**

:Configuration Directory:
    Location in which pyTD's :ref:`log <config.logging>`, :ref:`cached
    tokens <auth.cache>` (if using on-disk caching), and :ref:`SSL certificate and
    key<config.ssl>` are stored

:SSL Certificate and Key:
    If using local web server authentication (script applications), a
    self-signed SSL certificate and key are needed.

**User Agent** - ``api``

:Consumer Key \& Callback URL:
    TD Ameritrade authorization credentials

:Token Caching:
    Storage of authentication tokens. Can be cached *on-disk* or *in-memory*.

:Request Parameters:
    Specify how requests should be be made. These include ``retry_count``, ``pause``, and ``session``.

**Logging**

:Log Level:
    Logging level of pyTD. The ``logging`` module handles pyTD's logging.

.. _config.environment:

Configuring Environment
-----------------------

.. _config.config_dir:

Configuration Directory
~~~~~~~~~~~~~~~~~~~~~~~

By default, pyTD creates the directory ``.tdm`` in your home directory, which
serves as the default location for on-disk token caching, pyTD's log, and your SSL
certificate and key.

To specify a custom configuration directory, store such directory's *absolute*
path in the environment variable ``TD_CONFIG_DIR``:

.. code:: bash

    $ export TD_CONFIG_DIR=</path/to/directory>

replacing the bracketed text with your absolute path.

.. _config.ssl:

SSL Certificate and Key
~~~~~~~~~~~~~~~~~~~

.. seealso:: :ref:`What is a self-signed SSL Certificate?`

.. _config.ssl_auto:

Automatic
^^^^^^^^^

To generate the self-signed SSL key and certificate needed for local web server
authentication, use the top-level ``configure`` function:

.. code:: python

    from pyTD import configure

    configure()

This function will prompt creation of a self-signed SSL key and certificate,
which will both be placed in your :ref:`Configuration Directory`.

.. _config.ssl_manual:

Manual
^^^^^^

The SSL key and certificate can be created manually with the
following OpenSSL command:

.. code:: bash

    $ openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem

Place the generated key and certificate in the ``ssl`` sub-directory of your
:ref:`config.config_dir`.

.. _config.environment-variables:

Setting Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MacOS/Linux
^^^^^^^^^^^

To set the environment variables for your Consumer Key and Callback URL, use the
following command:

.. code:: bash

    $ export TD_CONSUMER_KEY='<YOUR_CONSUMER_KEY>'
    $ export TD_CALLBACK_URL='<YOUR_CALLBACK_URL>'

replacing the bracketed text with your information.

.. _config.all_in_one:


The All-in-One Solution: ``pyTD.configure``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pyTD provides the top-level function ``pyTD.configure`` which handles all
configuration necessary to make an authenticated query.

.. autofunction:: pyTD.configure



.. _config.user_agent:

Configuring User Agent
----------------------

.. _config.default-api:

There are three ways to configure your user agent:

1. **Let pyTD do it for you**. So long as you have your :ref:`Configuration
Directory` set up, simply run any pyTD function or method and pyTD will create
an ``api`` object for you, defaulting to an on-disk token cache.

.. code:: python

    from pyTD.market import get_quotes

    get_quotes("AAPL")

2. **Create a non-global API object**

Either pass the required parameters individually:

.. code:: python

    from pyTD.api import api
    from pyTD.market import get_quotes

    consumer_key = "TEST@AMER.OAUTHAP"
    callback_url = "https://localhost:8080"

    my_api = api(consumer_key=consumer_key, callback_url=callback_url)

    get_quotes("AAPL", api=my_api)

Or pass a pre-instantiated dictonary:

.. code:: python

    from pyTD.api import api
    from pyTD.market import get_quotes

    params = {
        "consumer_key": "TEST@AMER.OAUTHAP",
        "callback_url": "https://localhost:8080"
    }

    my_api = api(params)

    get_quotes("AAPL", api=my_api)

3. **Use** ``pyTD.configure``:

.. code:: python

    from pyTD import configure
    from pyTD.market import get_quotes

    consumer_key = "TEST@AMER.OAUTHAP"
    callback_url = "https://localhost:8080"

    configure(consumer_key=consumer_key, callback_url=callback_url)

    get_quotes("AAPL")

The ``api`` object
~~~~~~~~~~~~~~~~~~

The ``api`` object serves as the user agent for all requests to the TD
Ameritrade Developer API. The ``api`` object:

1. Manages configuration (directory, SSL, Consumer Key, Callback URL)
2. Connects to the token cache
3. Verifies, validates, and handles authentication and authorization.


.. autoclass:: pyTD.api.api



.. _config.logging:

Configuring Logging
-------------------

pyTD uses Python's `logging
<https://docs.python.org/3/library/logging.html>`__ module to log its activity
for both informational and debugging purposes.

By default, a log is kept in pyTD's :ref:`Configuration Directory` and named
``pyTD.log``.

Setting the logging level
~~~~~~~~~~~~~~~~~~~~~~~~~

The console logging level of pyTD can be set in one of three ways:

1. **Using** ``pyTD.log_level``:

.. code:: python

    import pyTD

    pyTD.log_level = "DEBUG"

2. **Using** ``logging.setLevel``:

.. code:: python

    import logging

    logging.getLogger("pyTD").setLevel(logging.DEBUG)

3. **Using environment variables**

The environment variable ``TD_LOG_LEVEL`` will override any log level settings for the console logger.

.. code:: bash

    export TD_LOG_LEVEL='DEBUG'

.. _config.appendix:

Appendix
--------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

For reference, the following environment variables may be set to configure pyTD:

- ``TD_CONSUMER_KEY`` (required) - TD Ameritrade Developer application OAUTH ID
- ``TD_CALLBACK_URL`` (required) - TD Ameritrade Developer application Callback URL
- ``TD_CONFIG_DIR`` - for specifying a custom pyTD configuration directory (defaults to ~/.tdm)
- ``TD_STORE_TOKENS`` - set to false to disable on-disk authentication token
  caching
- ``TD_LOG_LEVEL`` - for specifying a console logging level for pyTD
