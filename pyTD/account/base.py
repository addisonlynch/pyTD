import logging

from pyTD.resource import Get, Post, Put, Delete

ORDER = 'orders'
SAVED_ORDER = 'savedOrders'
TRANSACTION = 'transactions'

logger = logging.getLogger(__name__)


class Account(Get, Post, Put, Delete):
    """
    Class for retrieving account information, including orders and transactions
    """
    STATUS_CODES = {
        403: "You don't have permission to access this account resource."
    }

    def __init__(self, account_id, retry_count=3, pause=0.5,
                 session=None, api=None):
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
        super(Account, self).__init__(api, retry_count, pause, session)
        self.account_id = int(account_id)
        self.info = super(Account, self).get()["securitiesAccount"]

    @property
    def endpoint(self):
        return 'accounts'

    @property
    def resource(self):
        return self.account_id

    def read(self, resource_type, resource_id, method='GET'):
        url = self._BASE_URL + '%s/%s/%s/%s' % (self.endpoint, self.resource,
                                                resource_type, resource_id)
        return url

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

    def get_order(self, order_id):
        """
        Retrieve information about an order

        Parameters
        ----------
        order_id: int
            TD Ameritrade order ID
        """
        return self.get(url=self.order_url(order_id))

    def get_orders(self):
        """
        Retrieve all orders for current account
        """
        return self.get(url=self.order_url())

    def cancel_order(self, order_id):
        """
        Cancels an order

        Parameters
        ----------
        order_id: int
            TD Ameritrade order ID
        """
        url = self.order_url(order_id)
        self.delete(url=url)
        logger.info("Order %s deleted." % order_id)
        return True

    def place_order(self, order):
        """
        Places an order

        Parameters
        ----------
        order_id: int
            TD Ameritrade order ID
        """
        self.post(url=self.order_url(), data=order)
        logger.info("Order placed successfully.")
        return

    def replace_order(self, old_order_id, new_order):
        """
        Replaces an order with another

        Parameters
        ----------
        old_order_id: int
            TD Ameritrade order ID to be replaced
        new_order_id: int
            TD Ameritrade order ID of replacement order
        """
        url = self.order_url(old_order_id)
        self.put(url=url, data=new_order)
        logger.info("%s successfully replaced." % old_order_id)
        return

    def create_saved_order(self, order):
        """
        Creates a saved order

        Parameters
        ----------
        order_id: int
            TD Ameritrade order ID
        """
        self.post(url=self.saved_order_url(), data=order)
        logger.info("Order placed successfully.")
        return

    def delete_saved_order(self, order_id):
        """
        Deletes a saved order

        Parameters
        ----------
        order_id: int
            TD Ameritrade order ID
        """
        url = self.saved_order_url(order_id)
        self.delete(url=url)
        logger.info("Saved order %s deleted." % order_id)
        return True

    def get_saved_order(self, order_id):
        """
        Gets a saved order

        Parameters
        ----------
        order_id: int
            TD Ameritrade order ID
        """
        return self.get(url=self.saved_order_url(order_id))

    def replace_saved_order(self, old_order_id, new_order):
        """
        Replaces a saved order with another

        Parameters
        ----------
        old_order_id: int
            TD Ameritrade order ID to be replaced
        new_order_id: int
            TD Ameritrade order ID of replacement order
        """
        url = self.saved_order_url(old_order_id)
        self.put(url=url, data=new_order)
        logger.info("%s successfully replaced." % old_order_id)
        return

    def get_transaction(self, transaction_id):
        """
        Retrieves a transaction by transaction number

        Parameters
        ----------
        transaction_id: int
            TD Ameritrade transaction ID
        """
        return self.read(TRANSACTION, transaction_id)

    def get_transactions(self):
        """
        Retrieves all transactions of the account
        """
        return self.read(TRANSACTION, '')

    def get_preferences(self):
        """
        Retrieves preferences of the account
        """
        return self.read("preferences", '')


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
