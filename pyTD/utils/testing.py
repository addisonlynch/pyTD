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

from pyTD.api import default_api
from pyTD.compat import HTTPError
from pyTD.utils.exceptions import ConfigurationError


def default_auth_ok():
    """
    Used for testing. Returns true if a default API object is authorized
    """
    global __api__
    if __api__ is None:
        try:
            a = default_api()
            return a.auth_valid
        except ConfigurationError:
            return False
    else:
        if __api__.refresh_valid is True:
            return True
        else:
            return False


class MockResponse(object):
    """
    Class for mocking HTTP response objects
    """

    def __init__(self, text, status_code, request_url=None,
                 request_params=None, request_headers=None):
        """
        Initialize the class

        Parameters
        ----------
        text: str
                A plaintext string of the response
        status_code: int
                HTTP response code
        url: str, optional
                Request URL
        request_params: dict, optional
                Request Parameters
        request_headers: dict, optional
                Request headers
        """
        self.text = text
        self.status_code = status_code
        self.url = request_url
        self.request_params = request_params
        self.request_headers = request_headers

    def json(self):
        import json
        return json.loads(self.text)

    def raise_for_status(self):
        # Pulled directly from requests source code
        reason = ''
        http_error_msg = ''
        if 400 <= self.status_code < 500:
            http_error_msg = u'%s Client Error: %s for url: %s' % (
                self.status_code, reason, self.url)

        elif 500 <= self.status_code < 600:
            http_error_msg = u'%s Server Error: %s for url: %s' % (
                self.status_code, reason, self.url)

        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)


MOCK_SSL_CERT = """\
-----BEGIN CERTIFICATE-----
MIIDtTCCAp2gAwIBAgIJAPuEP7NccyjCMA0GCSqGSIb3DQEBBQUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIEwpTb21lLVN0YXRlMSEwHwYDVQQKExhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMTgwNzAzMDIzODMwWhcNMTkwNzAzMDIzODMwWjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECBMKU29tZS1TdGF0ZTEhMB8GA1UEChMYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEA/S/ocvpHNqQvuVtKqZi4JJbWRmw0hG2rS8NwXsn7YBkvPydvc9+CX5ZC
Tdt93Hh2g6t07+EDjFQdWzuD1paKoLsjI3RTGM9OhY25AF13jsgdCORSetKiAuQy
zKWtzLJ7egfjj8ZQdaUKhRONqLYu8IbtcQFuuL+B49xwPIfafMCmy6US/R6maCTH
zeIw8LahV4ECM9NttfIJTkEkN/O8D30rJVZbpMhJHq+Y4rh94oBVW4JJMc+VZlHi
C9d6E9yIiUtcKSsOZkZ3FL0TNEm2dmzI69wufC53B6NynYFVA0yhtvRgOZYdoFX6
cMhk3Ciy7nFav+fdZ4PsJirATjtisQIDAQABo4GnMIGkMB0GA1UdDgQWBBRtfob1
mHz0mr5YHvSYQ728X4Sz7zB1BgNVHSMEbjBsgBRtfob1mHz0mr5YHvSYQ728X4Sz
76FJpEcwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgTClNvbWUtU3RhdGUxITAfBgNV
BAoTGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZIIJAPuEP7NccyjCMAwGA1UdEwQF
MAMBAf8wDQYJKoZIhvcNAQEFBQADggEBAMUq5ZcfIzJF4nk3HqHxyajJJZNUarTU
aizCqDcLSU+SgcrsrVu51s5OGpK+HhwwkY5uq5C1yv0tYc7e0V9e/dpANvUR5RMv
Tme60HfJKioqhzSaNSz87a3TZayYhnREVfA6UqVL6EQ2ArVeqnn+mmrZ/oU5TJ9T
Opwr8Kah78xnC/0iOWOR4IXliakNHdO0qqJIYlbpBxM7znYT6vPbvp/IQC7PA8qP
AMce1keJ5u462aCza6zp95sFhqneDlI9lh9EA31eUfPgvdNPfqQP40DCQGSnvdeU
fPm9pF9V4FSlznPyRJI4AgZOqpt580+GWTtYQBwPCqZSHq66f83Lmz4=
-----END CERTIFICATE-----
"""


MOCK_SSL_KEY = """\
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA/S/ocvpHNqQvuVtKqZi4JJbWRmw0hG2rS8NwXsn7YBkvPydv
c9+CX5ZCTdt93Hh2g6t07+EDjFQdWzuD1paKoLsjI3RTGM9OhY25AF13jsgdCORS
etKiAuQyzKWtzLJ7egfjj8ZQdaUKhRONqLYu8IbtcQFuuL+B49xwPIfafMCmy6US
/R6maCTHzeIw8LahV4ECM9NttfIJTkEkN/O8D30rJVZbpMhJHq+Y4rh94oBVW4JJ
Mc+VZlHiC9d6E9yIiUtcKSsOZkZ3FL0TNEm2dmzI69wufC53B6NynYFVA0yhtvRg
OZYdoFX6cMhk3Ciy7nFav+fdZ4PsJirATjtisQIDAQABAoIBAQChwFKj6gtG+FvY
8l7fvMaf8ZGRSh2/IQVXkNOgay/idBSAJ2SHxZpYEPnpHbnp+TfV5Nr/SWTn6PEc
UQhoNqL4DrZjNzTDW+XRYvp3Jj90g5oxDRU4jIqeiEWAArTnWnuSOaoDN3I9xqPS
4uwUhde1KK5XDNA8zXRhK3q04SIPogtgyzYY9D+6TVF/F+34jhFG6TDjnuIP9PwG
l6eY+b7q1zspcqAXFXVJ5xxhkI79zmH0SoVKEz7VAtqdDi3dKfsInexjiLET4ibV
YcBgW0PRA0ZDw10EOjDAOZBzr1jitUuQ3VJI8XaWQaWt33tD7iVEdwDJt88w0YIc
bgtlIIXlAoGBAP63Fl8OWhgtcjVg/+idQg08HM/Tv6Ri/jtpWTnPmQolW8bCqB7M
SIc0DkHKluqTzTkNFD890WgKGTjV5UFXMFREtrRQJuycIfHg0FvGCtpYVjtqqgjn
0IVHfGVJ5Q3mFeSqMj8cheb5Nk767P66gd2gTLTFgca0Wh1Vf1ykBY3DAoGBAP52
2PMXrTBKsssXGPmA4/0HVvd1f0JzEH4ithhYwSvkNfwv+EdW8hriNVj5LL4sMC4j
P2hZKC7c39paG4MVvBHQ9AhgrH97VXxFzjIECTx9VINyR3yxT5Nqn6ilmTR1gmty
gdlEztFVloUlGrfHh8cGTGI6J7eYFCnk7NzGrEJ7AoGANu7ZfkqkF47FkMmIp2wy
8JPESvYJ4LQQzFNeEN+6y7te3bDhfTLleXM6l+nPPmv92I3/jdwRK3TyF5XZyYu6
OpJPLPgUTPcnQvkPNpuxf4GJp2rLnPwRtozCQT38jlDO6+/gwkeugS/CDKqFLjKf
C2Mk59+oq2f9/1GPFDWzlO0CgYAW8XZMLMVTxlhqkVGSJXno9YF03GY2ApPpG44Z
kd8Q6wmnDFgxbnhzzhOLSyQqnWdWsZzk9qz11LpmQJucbRhA7vshyj2jXOZvRwf5
YH3Is3AsTeB+MKqBGyr8FLpEjZfNwkxM37RaEYJ5zMek7FukqT+315B/MDoZMOfe
XBdqAwKBgD1CoyKb7Cgcb8zEHMkVAPP7tljpO1/gzuXRSOp7G4blKK+fF40vSh79
azBtciC6VbBwUPRW4OY9qPqhOMA3DAgeJZBrCrEkQVHWqW2u0FOdJsMDz5TpDQSV
cHy9ZQCz9WDroSC21Z0BFJ8DKPXvFL/XjlCtpfBP7JFoAChm5MeW
-----END RSA PRIVATE KEY-----
"""
