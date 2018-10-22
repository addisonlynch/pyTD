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

import os
import logging

__author__ = 'Addison Lynch'
__version__ = '0.0.1'

DEFAULT_CONFIG_DIR = '~/.tdm'
CONFIG_DIR = os.path.expanduser(os.getenv("TD_CONFIG_DIR", DEFAULT_CONFIG_DIR))

DEFAULT_SSL_DIR = os.path.join(CONFIG_DIR, 'ssl')
PACKAGE_DIR = os.path.abspath(__name__)

BASE_URL = 'https://api.tdameritrade.com/v1/'
BASE_AUTH_URL = 'https://auth.tdameritrade.com/auth'

# routing for configure
from pyTD.api import configure # noqa

# Store logging level
log_level = "INFO"
LEVEL = getattr(logging, os.getenv("TD_LOG_LEVEL", log_level))

# Set logging level
logger = logging.getLogger(__name__)
logger.setLevel(LEVEL)

fh = logging.FileHandler(os.path.join(CONFIG_DIR, 'pyTD.log'), delay=True)
ch = logging.StreamHandler()
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(file_format)

console_format = logging.Formatter(
    '%(levelname)s - %(message)s')
ch.setFormatter(console_format)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
