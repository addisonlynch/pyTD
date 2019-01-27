import logging

from pyTD import BASE_URL
from pyTD.api import default_api


logger = logging.getLogger(__name__)


class _pyTD_base(object):

    _BASE_URL = BASE_URL

    def __init__(self, api=None):
        self.api = api or default_api()

    @property
    def params(self):
        return {}
