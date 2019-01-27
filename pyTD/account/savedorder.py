from pyTD import BASE_URL
from pyTD.account.order import Order


class SavedOrder(Order):

    ORDER_ID_KEY = "savedOrderId"

    @property
    def path(self):
        return "%s/accounts/%s/savedorders" % (BASE_URL, self.account_id)

    def delete(self, *args, **kwargs):
        return self.cancel(*args, **kwargs)


SavedOrder.convert_resources["savedOrder"] = SavedOrder
SavedOrder.convert_resources["savedOrders"] = SavedOrder
