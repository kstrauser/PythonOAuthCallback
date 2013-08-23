"""
OAuth callback handler for App.net
"""

import urllib
import urlparse

from . import CallbackHandler, PORT


TEMPLATE_SUCCESS = """
<html>
<head><title>Successfully authenticated</title></head>
<body><p>Thanks! You may close this window now.</p></body>
</html>
"""

TEMPLATE_FAIL = """
<html>
<head><title>Unable to authenticate</title></head>
<body><p>Something bad happened!</p></body>
</html>
"""

TEMPLATE_REDIRECT = """
<html>
<head>
<title>Redirecting</title>
<script>
window.location = window.location.toString().replace('#', '?');
</script>
</head>
</html>
"""


class AppDotNetHandler(CallbackHandler):
    """
    Answer authentication response requests from App.net
    """

    @staticmethod
    def auth_url(client_id, scope):  # pylint: disable=W0221
        """
        Return the App.net authentication URL for this client
        """
        return 'https://account.app.net/oauth/authenticate?' + \
            urllib.urlencode({
                'client_id': client_id,
                'response_type': 'token',
                'scope': scope,
                'redirect_uri': 'http://localhost:%d' % PORT,
            })

    def do_GET(self):
        """
        App.net authentication redirects encode the access_token in the URL
        fragment. URL fragments don't get passed to the web server, so this
        method won't initially be able to find the token.

        When it receives a path without a '?' in it to distinguish query
        parameters, it returns a page with JavaScript that rewrites that URL
        fragment into a query parameter and the redirects to that new address.

        When that new request comes through, the method can harvest the
        access_token and return it.
        """
        if '?' in self.path:
            querystring = urlparse.urlparse(self.path).query
            querydict = urlparse.parse_qs(querystring)
            try:
                token = querydict['access_token'][0]
            except KeyError:
                template = TEMPLATE_FAIL
            else:
                template = TEMPLATE_SUCCESS
                self.finish_with_result({'access_token': token})
        else:
            template = TEMPLATE_REDIRECT

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template)
        self.wfile.close()
