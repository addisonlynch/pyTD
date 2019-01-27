from pyTD import BASE_URL
from pyTD.resource import Update, Create


class Order(Update, Create):

    def __init__(self, attributes=None, api=None, account_id=None):
        super(Order, self).__init__(attributes=attributes, api=None)
        if account_id is None:
            raise ValueError("Must specify account id as account_id")
        self.account_id = account_id

    @property
    def path(self):
        return "%s/accounts/%s/orders" % (BASE_URL, self.account_id)

    def update_status(self, attributes=None):
        attributes = attributes or self.to_dict()
        order_id = attributes.get("order_id", None)
        if order_id is None:
            raise ValueError("Invalid order. Cannot update")
        url = "%s/%s" % (self.path, order_id)
        new_attributes = self.api.get(url=url)
        self.error = None
        self.merge(new_attributes)
        return self.success()


Order.convert_resources["order"] = Order
Order.convert_resources["orders"] = Order
