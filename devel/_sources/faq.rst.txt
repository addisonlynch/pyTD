.. _faq:

Frequently Asked Questions
==========================

.. _faq.oauth_20:

What is OAuth 2.0?
------------------

From `RFC 6749 <https://tools.ietf.org/html/rfc6749>`__:



   The OAuth 2.0 authorization framework enables a third-party
   application to obtain limited access to an HTTP service, either on
   behalf of a resource owner by orchestrating an approval interaction
   between the resource owner and the HTTP service, or by allowing the
   third-party application to obtain access on its own behalf.

In other words, OAuth 2.0 is the protocol that TD Ameritrade uses to help you
gain access to the Developer API (and your account). There are four roles in
this process:

1. **Resource Owner** - an entity capable of granting access to a protected
resource. **In this case, YOU**.

2. **Resource Server** - the server hosting the protected resources, capable of
accepting and responding to protected resource requests using access tokens.
**In this case, TD Ameritrade's servers**.

3. **Client** - An application making protected resource requests on behalf of
the resource owner and with its authorization. **In this case, pyTD (or an
application which uses it)**.

4. **Authorization Server** - The server issung access tokens to the client
after successfully authenticating the resource owner and obtaining
authorization. **In this case, your application or local authorization
server**.




.. _faq.callback-url:

What should my Callback URL be?
-------------------------------

This raises an important question: **What is a Callback URL?**

From `RFC 6749 <https://tools.ietf.org/html/rfc6749>`__:

   The authorization code is obtained by using an **authorization server**
   as an intermediary between the client and resource owner.  Instead of
   requesting authorization directly from the resource owner, **the client
   directs the resource owner to an authorization server** (via its
   user-agent as defined in [RFC2616]), which in turn directs the
   resource owner back to the client with the authorization code....

   ... **Because the resource owner only authenticates with the authorization
   server, the resource owner's credentials are never shared with the client**.

As explained in :ref:`What is OAuth 2.0?`, the resource owner is you - as you
have the access to your TD Ameritrade brokerage account. In order to prevent
your account credentials from being revealed, authentication is completed with
an **authorization server**.

Default ``pyTD`` behavior is to start this server locally, running on your
localhost (typically ``127.0.0.1``). If this is the case, your Callback URL
should be https://localhost:8080.


.. _faq.ssl-basics:

What is a self-signed SSL certificate?
--------------------------------------

An SSL certificate certifies the identity of an entity such as your local pyTD authentication server. **Self-signed SSL certificates** are signed by the same entity which they are certifying the identity of.

This may cause problems for some browsers, which will display messages such as "Your connection is not private" and "This site's security certificate is not trusted!". This is due to the fact that your application is not a trusted certificate authority.

.. _faq.create-ssl-cert-key:

How do I create a self-signed SSL certificate and key?
------------------------------------------------------

There are a number of different options for generating a self-signed SSL
certificate and key.

The easiest way: OpenSSL
~~~~~~~~~~~~~~~~~~~~~~~~

`OpenSSL <https://www.openssl.org/>`__ is an SSL/TLS toolkit which is useful
for generating SSL certificates. Once installed (see system-specific
installation instructions below), run the following command to generate key
and certificate files ``key.pem`` and ``cert.pem``:

.. code-block:: bash

  openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem


Installing OpenSSL
^^^^^^^^^^^^^^^^^^

**macOS**

Install using `Homebrew <https://brew.sh/>`__:

.. code-block:: bash

  brew update
  brew install openssl

**Linux**

OpenSSL is packaged with most Linux distributions


**Windows**

OpenSSL for Windows can be downloaded `here <http://gnuwin32.sourceforge.net/packages/openssl.htm>`__.


.. _faq.dev_account:

How do I get my Consumer Key and Callback URL?
----------------------------------------------

A TD Ameritrade Developer account and application are required in order to access the Developer API. **This is a separate account from TD Ameritrade Brokerage Accounts**. A TD Ameritrade Brokerage Account is **not required** to obtain a TD Ameritrade Developer Account.

To register for a TD Ameritrade Developer account, visit https://developer.tdameritrade.com/ and click "Register" in the top-right corner of the screen.

Creating an App
~~~~~~~~~~~~~~~

To create a new TD Ameritrade Developer Application, navigate to the "My Apps" page of your TD Ameritrade Developer Account:

.. figure:: _static/img/noapps.png

    My Apps Page

From here, click the "Add a new App" button:

.. figure:: _static/img/createapp.png

    Creating an app

You will be prompted to enter the following fields:

1) **App Name** - desired application name
2) **Callback URL** - also known as Callback URL, this is the callback address to complete authorization
3) **OAuth User ID** - a unique ID that will be used to create your full OAauth ID
4) **App Description** - a description of your application

After completing the form, your application will be created. By clicking on the application in the "My Apps" page, you can display information about it:

.. figure:: _static/img/appinfo.png

    App Info

The **Consumer Key** field is your **Consumer Key**. Your **Callback URL** is the **Callback URL** which you entered at the app's creation.

.. note:: To change the Callback URL (Callback URL) of your application, you must delete the application and create a new one. This is a caveat of the TD Ameritrade registration process.


.. _faq.script:

What is a Script Application?
-----------------------------

A script application is simply an application that is run as a script from your
local environment. This may be a stand-alone script that is run which uses pyTD
or command-line invocation of pyTD, such as running:

.. code-block:: python

  >>> from pyTD.market import get_quotes
  >>> get_quotes("AAPL")

in an interactive Python shell.


.. _faq.cusip:

What is a CUSIP ID?
-------------------

A CUSIP is a nine-character alphanumeric code that identifies a North American
financial security.

Simply put, CUSIPs are unique identifiers for a number of financial instruments
including common stocks, bonds, and other equities.

.. _faq.cusip-examples:

Examples
~~~~~~~~

- Apple Inc.: 03783100
- Cisco Systems: 17275R102
- Google Inc.: 38259P508
- Microsoft Corporation: 594918104
- Oracle Corporation: 58389X105

.. _faq.token_storage:

Is it safe to save my authentications on-disk?
----------------------------------------------

.. note:: TODO
