import logging

from pyTD.account.order import Order
from pyTD.base import _pyTD_base

ORDER = 'orders'
SAVED_ORDER = 'savedOrders'
TRANSACTION = 'transactions'

logger = logging.getLogger(__name__)


class Account(_pyTD_base):
    """
    Class for retrieving account information, including orders and transactions
    """
    STATUS_CODES = {
        403: "You don't have permission to access this account resource."
    }

    def __init__(self, account_id, api=None):
        """
        Initialize the class.

        Parameters
        ----------
        account_id: int or str
            TD Ameritrade account ID
        retry_count: int, default 3, optional
            Desired number of retries if a request fails
        pause: float, default 0.5, optional
            Pause time between retry attempts
        session: requests_cache.session, default None, optional
            A cached requests-cache session
        """
        super(Account, self).__init__(api)
        self.account_id = int(account_id)
        self.orders = []
        self.update_info()

    @property
    def endpoint(self):
        return 'accounts'

    @property
    def resource(self):
        return self.account_id

    @property
    def url(self):
        return "%s/accounts/%s" % (self._BASE_URL, self.account_id)

    def update_info(self):
        self.info = self.api.get(url=self.url)["securitiesAccount"]

    def order_url(self, order_id=None):
        base = "%saccounts/%s/orders" % (self._BASE_URL, self.account_id)
        if order_id:
            return "%s/%s" % (base, order_id)
        return base

    def saved_order_url(self, order_id=None):
        base = "%saccounts/%s/savedorders" % (self._BASE_URL, self.account_id)
        if order_id:
            return "%s/%s" % (base, order_id)
        return base

    def send(self, resource_tpye, resource_id, method='POST'):
        pass

    def read(self):
        return self.api.get(url=self.url, params=self.params)

    @property
    def type(self):
        """
        Retrieves account type (CASH or MARGIN)
        """
        return self.info['type']

    @property
    def id(self):
        """
        Retrieves account ID
        """
        return self.info['accountID']

    def get_orders(self):
        url = self.url + "/orders"
        raw_data = self.api.get(url=url)
        for order in raw_data:
            self.orders.append(Order(order, account_id=self.account_id,
                                     api=self.api))
        return self.orders


def get_account(*args, **kwargs):
    """
    Returns account information for an account

    Parameters
    ----------
    account_id: int or str
        TD Ameritrade account ID
    kwargs: optional
        Additional request parameters (see _TDBase class)
    """
    return Account(*args, **kwargs).read()
