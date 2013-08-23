"""
Provide a standard framework for writing OAuth callback handlers
"""

import abc
import webbrowser
import BaseHTTPServer

PORT = 8000


class CallbackHandler(BaseHTTPServer.BaseHTTPRequestHandler, object):
    """
    Abstract base class for handling web requests from a browser fetching
    a callback URL
    """

    __metaclass__ = abc.ABCMeta

    @classmethod
    def fetch_access_token(cls, **kwargs):
        """
        Open the user's web browser to the auth URL then run a web server to
        accept and process its callback
        """
        webbrowser.open(cls.auth_url(**kwargs))

        httpd = BaseHTTPServer.HTTPServer(("", PORT), cls)
        httpd.result = None

        while httpd.result is None:
            httpd.handle_request()

        httpd.server_close()

        return httpd.result

    @staticmethod
    @abc.abstractmethod
    def auth_url(**kwargs):
        """
        Return the system-specific authentication endpoint URL
        """

    @abc.abstractmethod
    def do_GET(self):  # pylint: disable=C0103
        """
        Override this to implement system-specific callback logic
        """
        self._finish_with_result({'token': 'foobar'})

    def _finish_with_result(self, value):
        """
        Return the value to the server and signal it to stop answering queries
        """
        self.server.result = value
