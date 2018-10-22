.. _quickstart:

Quick Start Guide
=================

.. note:: This Quick Start guide assumes the use of a :ref:`Script
    Application <What is a Script Application?>`. See :ref:`Authentication` for
    more information about using
    **installed** applications and **web** applications.

In this section, we go over everything you need to know to start building
scripts, or bots using pyTD, the Python TD Ameritrade Developer API SDK.
It's fun and easy. Let's get started.

Prerequisites
-------------

:Python Knowledge: You need to know at least a little Python to use pyTD; it's
                   a Python wrapper after all. PRAW supports `Python 2.6
                   to 2.7`_,
                   and `Python 3.4 to 3.7`_.

:TD Ameritrade Knowledge: A basic understanding of how TD Ameritrade's
                   Developer APIs work is a must. It is recommended that you read
                   through the `TD Ameritrade documentation`_ before starting
                   with pyTD.

:TD Ameritrade Developer Account: This is a **separate account** from your TD
                      brokerage accounts(s).

.. _`Python 2.6 to 2.7`: https://docs.python.org/2/tutorial/index.html
.. _`Python 3.4 to 3.7`: https://docs.python.org/3/tutorial/index.html
.. _`TD Ameritrade documentation`: https://developer.tdameritrade.com/apis

.. _quickstart.common_tasks:


Step 1 - Obtain an Consumer Key and Callback URL
--------------------------------------------

.. seealso:: For a more detailed tutorial on setting up a TD Ameritrade
    Developer Account, creating an application, or obtaining an Consumer Key and
    Callback URL, see :ref:`How do I get my Consumer Key and Callback URL?`.

1. From your TD Ameritrade Developer Account, **create a new application**
using the "Add App" button in your profile. Enter the following information
when prompted:

* **App Name** - desired application name (can be anything)
* **Callback URL** - the address that your authentication information will be forwarded to complete authentication of your script application (https://localhost:8080
  is easiest). See :ref:`What should my Callback URL be?` for more information
  on choosing a Callback URL.
* **OAuth User ID** - unique ID that will be used to create your consumer key
  (can be anything)
* **App Description** - description of your application (can be anything)

2. Once your application has been created, store its **Consumer Key** and **Callback URL**
in the environment variables ``TD_CONSUMER_KEY`` and ``TD_CALLBACK_URL``:

.. code-block:: bash

    $ export TD_CONSUMER_KEY=TEST@AMER.OAUTHAP # Your Consumer Key
    $ export TD_CALLBACK_URL=https://localhost:8080 # Your Callback URL

.. note:: If you are unfamiliar with environment variables or unable to
    set them on your system, see :ref:`Configuring Environment` for more
    configuration options.



Step 2 - Run ``pyTD.configure``
-------------------------------


The easiest (and recommended) way configure ``pyTD`` is using
``pyTD.configure``.


.. code-block:: python

  import pyTD
  pyTD.configure()

This function does the following:

1. Creates a **configuration directory** (defaults to ``.tdm`` in your home
directory). The location can be chosen manually by setting the environment
variable ``TD_CONFIG_DIR``. This directory is the location in which pyTD's
:ref:`log<config.logging>`, :ref:`cached tokens <auth.cache>` (if using on-disk
caching), and :ref:`SSL certificate and key<config.ssl>` are stored.

2. Generates a **self-signed SSL certificate \& key** and places them in the
``ssl`` directory within your configuration directory.

.. warning::  If using MacOS, you may not be able to generate the certificate
              and key using ``pyTD.configure``. See :ref:`Generating an SSL Certificate and Key <config.ssl_manual>` for
              more information and instructions on how to generate the
              certificate manually.

.. note::
  When called with no arguments, ``pyTD.configure`` requires :ref:`setting environment
  variables` ``TD_CONSUMER_KEY`` and ``TD_CALLBACK_URL`` to your app's Consumer Key and
  Callback URL. These can also be passed to ``pyTD.configure`` instead:

  .. code:: python

      import pyTD

      consumer_key='TEST@AMER.OAUTHAP'
      callback_url='https://localhost:8080'

      pyTD.configure(consumer_key=consumer_key, callback_url=callback_url)

  ``pyTD.configure`` will set the environment variables automatically for the
  **current session only**.

.. _`documentation`: https://addisonlynch.github.io/pytd/stable/faq.html#what-is-a-td-ameritrade-developer-account
.. _`Generating an SSL Key/Certificate`: https://addisonlynch.github.io/pytd/stable/configuration.html#generating-an-ssl-key-certificate
.. _`docs`:  https://addisonlynch.github.io/pytd/stable/configuration.html#the-all-in-one-solution-pytd-configure
.. _`configuration directory`: https://addisonlynch.github.io/pytd/stable/configuration.html#configuration-directory

.. _quickstart.authenticate-app:

Step 3 - Authenticate Your Application
--------------------------------------


The simplest way to authorize and authenticate pyTD is by calling any function which
returns data. For example ``get_quotes`` from ``pyTD.market``
will automatically prompt you to obtain a new refresh token if you have not
obtained one or your refresh token has expired:


.. code-block:: python

    from pyTD.market import get_quotes

    get_quotes("AAPL")
    # WARNING:root:Need new refresh token.
    # Would you like to authorize a new refresh token? [y/n]:

Selecting ``y`` will open a browser for you to authorize your application:

.. figure:: _static/img/authprompt.png

Select "AUTHORIZE" to redirect to a TD Ameritrade login prompt:

.. figure:: _static/img/tdlogin.png

From here, log in to your TD Ameritrade Brokerage Account. Once logged in, the following page will be displayed:

.. figure:: _static/img/tdallow.png

Select "Allow" to authorize your application. pyTD will handle receiving the tokens and authorization code behind the scenes, and if retrieval is successful, the results of your original query will display on screen.


Step 4 - Go!
------------

You're now all set up to query TD Ameritrade's Developer APIs!

.. seealso:: For more usage tutorials and examples, see :ref:`Tutorials
  <tutorial_basics>`
