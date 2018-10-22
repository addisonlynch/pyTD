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

import sys
from distutils.version import LooseVersion

import pandas as pd

PY3 = sys.version_info >= (3, 0)

PANDAS_VERSION = LooseVersion(pd.__version__)

PANDAS_0190 = (PANDAS_VERSION >= LooseVersion('0.19.0'))
PANDAS_0230 = (PANDAS_VERSION >= LooseVersion('0.23.0'))

if PANDAS_0190:
    from pandas.api.types import is_number
else:
    from pandas.core.common import is_number  # noqa

if PANDAS_0230:
    from pandas.core.dtypes.common import is_list_like
else:
    from pandas.core.common import is_list_like  # noqa

if PY3:
    from urllib.error import HTTPError
    from urllib.parse import urlparse, urlencode, parse_qs
    from io import StringIO
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from mock import MagicMock
else:
    from urllib2 import HTTPError  # noqa
    from urlparse import urlparse, parse_qs  # noqa
    from urllib import urlencode  # noqa
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  # noqa
    import StringIO  # noqa
    from mock import MagicMock # noqa
