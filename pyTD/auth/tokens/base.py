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

import datetime

from pyTD.utils import to_timestamp


class Token(object):
    """
    Token object base class.

    Parameters
    ----------
    token: str
        Token value
    access_time: int
    expires_in: int

    """
    def __init__(self, options=None, **kwargs):

        kwargs.update(options or {})

        self.token = kwargs['token']
        self.access_time = kwargs['access_time']
        self.expires_in = kwargs['expires_in']

    def __dict__(self):
        return {
            "token": self.token,
            "access_time": self.access_time,
            "expires_in": self.expires_in
        }

    def __eq__(self, other):
        if isinstance(other, Token):
            t = self.token == other.token
            a = self.access_time == other.access_time
            e = self.expires_in == other.expires_in
            return t and a and e

    def __ne__(self, other):
        if isinstance(other, Token):
            t = self.token == other.token
            a = self.access_time == other.access_time
            e = self.expires_in == other.expires_in
            return t and a and e

    def __repr__(self):
        fmt = ("Token(token= %s, access_time = %s, expires_in = %s)")
        return fmt % (self.token, self.access_time, self.expires_in)

    def __str__(self):
        return self.token

    @property
    def expiry(self):
        return self.access_time + self.expires_in

    @property
    def valid(self):
        now = to_timestamp(datetime.datetime.now())
        return True if self.expiry > now else False
