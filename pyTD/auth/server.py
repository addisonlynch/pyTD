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

import codecs
import datetime
import json
import logging
import os
import requests
import ssl

from pyTD import BASE_AUTH_URL, DEFAULT_SSL_DIR, PACKAGE_DIR
from pyTD.compat import HTTPServer, BaseHTTPRequestHandler
from pyTD.compat import urlparse, urlencode, parse_qs
from pyTD.utils import to_timestamp
from pyTD.utils.exceptions import AuthorizationError

logger = logging.getLogger(__name__)


class Handler(BaseHTTPRequestHandler):

    STATIC_DIR = os.path.join(PACKAGE_DIR, '/auth/_static/')

    @property
    def auth_link(self):
        params = {
            "response_type": "code",
            "redirect_url": self.server.callback_url,
            "client_id": self.server.consumer_key,
        }
        return '%s?%s' % (BASE_AUTH_URL, urlencode(params))

    def do_GET(self):
        if self.path.endswith(".css"):
            f = open("pyTD/auth/_static/style.css", 'r')
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(f.read().encode())
            f.close()
            return

        self._set_headers()
        path, _, query_string = self.path.partition('?')
        try:
            code = parse_qs(query_string)['code'][0]
        except KeyError:
            f = codecs.open("pyTD/auth/_static/auth.html", "r", "utf-8")
            auth = f.read()
            link = auth.format(self.auth_link)
            self.wfile.write(link.encode('utf-8'))
            f.close()
        else:
            self.server.auth_code = code
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'refresh_token': '', 'grant_type': 'authorization_code',
                    'access_type': 'offline', 'code': self.server.auth_code,
                    'client_id': self.server.consumer_key,
                    'callback_url': self.server.callback_url}
            now = to_timestamp(datetime.datetime.now())
            authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/'
                                      'token', headers=headers, data=data)
            try:
                json_data = authReply.json()
                json_data["access_time"] = now
                self.server._store_tokens(json_data)
            except ValueError:
                msg = json.dumps(json_data)
                logger.Error("Tokens could not be obtained")
                logger.Error("RESPONSE: %s" % msg)
                raise AuthorizationError("Authorization could not be "
                                         "completed")
            success = codecs.open("pyTD/auth/_static/success.html", "r",
                                  "utf-8")

            self.wfile.write(success.read().encode())
            success.close()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()


class TDAuthServer(HTTPServer):
    """
    HTTP Server to handle authorization
    """
    def __init__(self, consumer_key, callback_url, retry_count=3):
        self.consumer_key = consumer_key
        self.callback_url = callback_url
        self.parsed_url = urlparse(self.callback_url)
        self.retry_count = retry_count
        self.auth_code = None
        self.tokens = None
        self.ssl_key = os.path.join(DEFAULT_SSL_DIR, 'key.pem')
        self.ssl_cert = os.path.join(DEFAULT_SSL_DIR, 'cert.pem')
        super(TDAuthServer, self).__init__(('localhost', self.port),
                                           Handler)
        self.socket = ssl.wrap_socket(self.socket, keyfile=self.ssl_key,
                                      certfile=self.ssl_cert,
                                      server_side=True)

    @property
    def hostname(self):
        return "%s://%s" % (self.parsed_url.scheme, self.parsed_url.hostname)

    @property
    def port(self):
        return self.parsed_url.port

    def _store_tokens(self, tokens):
        self.tokens = tokens

    def _wait_for_tokens(self):
        count = 0
        while count <= self.retry_count and self.tokens is None:
            self.handle_request()
        if self.tokens:
            return self.tokens
        else:
            raise AuthorizationError("The authorization could not be "
                                     "completed.")
