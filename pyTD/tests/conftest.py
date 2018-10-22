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

# flake8: noqa
import pytest

# fixture routing
from pyTD.tests.fixtures import sample_oid
from pyTD.tests.fixtures import sample_uri
from pyTD.tests.fixtures import valid_refresh_token, valid_access_token
from pyTD.tests.fixtures import set_env, del_env
from pyTD.tests.fixtures import valid_cache, invalid_cache

# mock responses routing
from pyTD.tests.fixtures.mock_responses import mock_400

from pyTD.utils.testing import default_auth_ok


def pytest_runtest_setup(item):
    envmarker = item.get_marker("webtest")
    auth_ok = default_auth_ok()
    if envmarker is not None and auth_ok is False:
            pytest.skip("Valid access required.")
