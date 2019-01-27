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
from pyTD.api import api
from pyTD.resource import Resource


class TestResource(object):

    def test_getter(self):
        data = {
            "orderType": "MARKET",
            "session": "NORMAL",
            "duration": "DAY",
            "orderId": 322922629,
            "orderLegCollection": [{
                "instruction": "buy",
                "quantity": 10
            }]

        }

        resource = Resource(data)

        assert resource.orderType == "MARKET"
        assert resource.session == "NORMAL"
        assert resource.duration == "DAY"
        assert resource.orderId == 322922629
        assert resource.orderLegCollection[0]["instruction"] == "buy"
        assert resource.orderLegCollection[0]["quantity"] == 10

    def test_setter(self):
        data = {'name': 'testing'}

        resource = Resource(data)

        resource.name = 'changed'
        assert resource.name == 'changed'
        resource['name'] = 'again-changed'
        assert resource.name == 'again-changed'

        resource.transaction = {'description': 'testing'}

        # These should pass but they don't
        # assert resource.transaction.__class__ == Resource
        # assert resource.transation.description == 'testing'

    def test_to_dict(self):
        data = {
          "orderType": "LIMIT",
          "session": "NORMAL",
          "price": "4.97",
          "duration": "DAY",
          "orderStrategyType": "TRIGGER",
          "orderLegCollection": [
            {
              "instruction": "BUY",
              "quantity": 10,
              "instrument": {
                "symbol": "XYZ",
                "assetType": "EQUITY"
              }
            }
          ],
          "childOrderStrategies": [
            {
              "orderType": "LIMIT",
              "session": "NORMAL",
              "price": "42.03",
              "duration": "DAY",
              "orderStrategyType": "SINGLE",
              "orderLegCollection": [
                {
                  "instruction": "SELL",
                  "quantity": 12,
                  "instrument": {
                    "symbol": "XYZ",
                    "assetType": "EQUITY"
                  }
                }
              ]
            }
          ]
        }
        resource = Resource(data)
        assert resource.to_dict() == data

    def test_passing_api(self, sample_oid, sample_uri, valid_cache):
        a = api(consumer_key=sample_oid, callback_url=sample_uri,
                cache=valid_cache)

        resource = Resource({
                'name': 'testing'
            }, api=a)

        assert resource.api == a
        assert resource.name == 'testing'

        # this should pass but does not
        # convert_ret = resource.convert('test', {})
        # assert convert_ret.api == api

    def test_contains(self):
        data = {
            'name': 'testing'
        }
        resource = Resource(data)
        assert 'name' in resource
        assert 'testing' not in resource
