.. _auth:

Authentication
==============

TD Ameritrade uses `OAuth 2.0 <https://oauth.net/2/>`__ to authorize and
authenticate requests.


.. seealso:: Not familiar with OAuth 2.0? See :ref:`What is OAuth 2.0?` for an overview of OAuth Authentication and Authorization.

.. _auth.overview:

Overview
--------

1. Send Consumer Key and Callback URL from your app's details to TD Ameritrade
2. Open web browser to TD Ameritrade, **login to TD Ameritrade Brokerage Account**
3. Send authorization code to receive refresh and access tokens
4. Refresh and access tokens are stored in your ``api`` instance's ``cache`` (either ``DiskCache`` or ``MemCache``)

.. _auth.script:

Script Application
------------------

**Script** applications are the simplest type of application to work with
because they don't involve any sort of callback process to obtain an
``access_token``.

TD Ameritrade requires that you provide a Callback URL when registering your application -- ``http://localhost:8080`` is a simple one to use.

.. seealso:: :ref:`What should my Callback URL be?`


pyTD provides a simple web server, written in pure Python, to handle
authentication with TD Ameritrade. If used for authentication, this server will run on your localhost (127.0.0.1) and receive your authorization code at your specified Callback URL.

.. _auth.web:

Web Application
---------------

If you have a **web** application and want to be able to access pyTD
Enter the appropriate Callback URL and configure that endpoint to complete the code flow.


.. _auth.installed:

Installed Application
---------------------



.. _auth.cache:

Token Caching
-------------

.. warning:: To enable persistent access to authentication tokens across sessions, pyTD stores tokens on-disk by default. **Storing tokens on-disk may pose a security risk to some users.** See :ref:`Is it safe to save my authentications on-disk?` for more information.

By default, tokens are stored *on-disk* in the :ref:`Configuration
Directory`, though they can also be stored *in-memory*. There are two ways to select a token storage method:

1. **Environment Variable** (recommended) - set the ``TD_STORE_TOKENS`` variable:

.. code-block:: bash

    $ export TD_STORE_TOKENS=False

2. Pass ``store_tokens`` keyword argument when creating an ``api`` instance to set token storage temporarily:

.. code-block:: python

    from pyTD.api import api

    oid = "TEST@AMER.OAUTHAP"
    uri = "https://localhost:8080"

    a = api(consumer_key=oid, callback_url=uri, store_tokens=False)

When ``store_tokens`` is set to ``False``, any stored tokens will be freed from memory when the program exits.


Caches
~~~~~~

In-Memory - ``MemCache``
^^^^^^^^^^^^^^^^^^^^^^^^

The ``MemCache`` class provides in-memory caching for authorization tokens.

**Important** - the stored tokens will be freed from memory when your program exits.

.. autoclass:: pyTD.cache.MemCache


On-Disk - ``DiskCache``
^^^^^^^^^^^^^^^^^^^^^^^

To store auth tokens on-disk, the ``DiskCache`` class is provided. When passed an absolute path, ``DiskCache`` creates the necessary directories and instantiates an empty cache file.

.. autoclass:: pyTD.cache.DiskCache


.. todo:: ``SQLCache`` - caching auth tokens in a sqllite database.




