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

import logging


logger = logging.getLogger(__name__)


class AuthorizationError(Exception):
    """
    This error is thrown when an error with authorization occurs
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SSLError(AuthorizationError):
    pass


class TDQueryError(Exception):
    def __init__(self, response=None, content=None, message=None):
        self.response = response
        self.content = content
        self.message = message

    def __str__(self):
        message = self.message
        if hasattr(self.response, 'status_code'):
            message += " Response status: %s." % (self.response.status_code)
        if hasattr(self.response, 'reason'):
            message += " Response message: %s." % (self.response.reason)
        if hasattr(self.response, 'text'):
            message += " Response text: %s." % (self.response.text)
        if hasattr(self.response, 'url'):
            message += " Request URL: %s." % (self.response.url)
        if self.content is not None:
            message += " Error message: %s" % str(self.content)
        return message


class ClientError(TDQueryError):

    _DEFAULT = "There was a client error with your request."

    def __init__(self, response, content=None, message=None):
        pass


class ServerError(TDQueryError):
    pass


class ResourceNotFound(TDQueryError):
    pass


class ValidationError(TDQueryError):
    pass


class ForbiddenAccess(TDQueryError):
    pass


class ConnectionError(TDQueryError):
    pass


class Redirection(TDQueryError):
    pass


class ConfigurationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CacheError(Exception):
    pass
