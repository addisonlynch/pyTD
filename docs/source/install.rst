.. _install:


Installing pyTD
===============

pyTD supports Python 2.6, 2.7, 3.4, 3.5, 3.6, and 3.7. The recommended
installation method is via ``pip``:

.. code-block:: bash

    $ pip install pyTD


Below are the options for installing pyTD.

.. warning:: After pyTD is installed, it must be configured. See the pyTD :ref:`Quick Start Guide` for more information.

.. _install.dependencies:

Dependencies
------------

- requests
- pandas

For testing requirements, see `testing <testing.html>`__.

Installation
------------

The recommended installation method is ``pip``. For more information about
installing Python and pip, see "The Hitchhiker's Guide to Python" `Installation
Guides <http://docs.python-guide.org/en/latest/starting/installation/>`__.

Stable Release
~~~~~~~~~~~~~~

.. code:: bash

    $ pip install pyTD


Development Version
~~~~~~~~~~~~~~~~~~~


.. code:: bash

    $ pip install git+https://github.com/addisonlynch/pyTD.git

or

.. code:: bash

     $ git clone https://github.com/addisonlynch/pyTD.git
     $ cd pyTD
     $ pip install .

Older Versions
~~~~~~~~~~~~~~

.. code:: bash

    $ pip install pyTD=0.0.1

virtualenv
----------

The use of
`virtualenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
is **highly** recommended as below:

.. code:: bash

    $ pip install virtualenv
    $ virtualenv env
    $ source env/bin/activate
