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

from pyTD.resource import Get
from pyTD.utils.exceptions import ResourceNotFound


class Instruments(Get):
    """
    Class for retrieving instruments
    """
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol
        self.output_format = kwargs.get("output_format", "pandas")
        self.projection = kwargs.get("projection", "symbol-search")
        super(Instruments, self).__init__(kwargs.get("api", None))

    @property
    def url(self):
        return "%s/instruments" % self._BASE_URL

    @property
    def params(self):
        return {
            "symbol": self.symbol,
            "projection": self.projection
        }

    def _convert_output(self, out):
        import pandas as pd
        if self.projection == "fundamental":
            return pd.DataFrame({self.symbol:
                                 out[self.symbol]["fundamental"]}).T
        return pd.DataFrame(out).T

    def execute(self):
        data = self.get()
        if not data:
            raise ResourceNotFound("Instrument data for %s not"
                                   " found." % self.symbol)
        if self.output_format == "pandas":
            return self._convert_output(data)
        else:
            return data
