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

from pyTD.auth.tokens import EmptyToken


def surface_property(api_property_name, docstring=None):
    def getter(self):
        return self._get(api_property_name) or EmptyToken()

    def setter(self, value):
        if isinstance(value, EmptyToken):
            self._set(api_property_name, None)
        else:
            self._set(api_property_name, value)

    return property(getter, setter, doc=docstring)


class TokenCache(object):
    """
    Base class for auth token caches
    """
    refresh_token = surface_property("refresh_token")
    access_token = surface_property("access_token")

    def __init__(self):
        self._create()

    def clear(self):
        raise NotImplementedError

    def _create(self):
        raise NotImplementedError

    def _exists(self):
        raise NotImplementedError

    def _get(self):
        raise NotImplementedError

    def _set(self):
        raise NotImplementedError
