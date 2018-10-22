.. _testing:


Testing
=======


.. _testing.environment:

Setting Up a Testing Environment
--------------------------------

1. Install the testing :ref:`dependencies`

 .. code:: bash

    $ pip3 install -r requirements-test.txt

2. Run the tests

 In the pyTD root directory, there is a shell script ``test.sh``. This script
 first verifies flake8 compliance, then runs all tests with pytest.

.. _testing.writing-tests:

Writing Tests
-------------

Marking
~~~~~~~

All tests which require HTTP requests which are not mocked should be
marked with ``pytest.mark.webtest``. These tests will be automatically skipped
if pyTD has not been properly configured or does not have a valid access token
(this is verified through ``pyTD.api.default_auth_ok``).


Fixtures
~~~~~~~~

A number of fixtures are used to provide instantiated objects (``api``,
tokens, etc.) as well as parametrize tests. These fixtures can be found in the
``fixtures`` directory.

.. seealso:: `pytest Fixtures Documentation
 <https://docs.pytest.org/en/latest/fixture.html>`__


.. _testing.dependencies:

Testing Dependencies
--------------------

Tests
~~~~~

- `pytest <https://pytest.org/>`__
- `tox <https://tox.readthedocs.io/en/latest/>`__
- `flake8 <http://flake8.pycqa.org/en/latest/>`__


Documentation
~~~~~~~~~~~~~

- `sphinx <http://www.sphinx-doc.org/en/master/>`__
- `sphinx-autobuild <https://pypi.org/project/sphinx-autobuild/>`__
- `sphinx-rtd-theme <https://github.com/rtfd/sphinx_rtd_theme>`__
- `ipython <https://ipython.org/>`__
- `matplotlib <https://matplotlib.org/>`__
