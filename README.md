PythonOAuthCallback
===================

*A local webserver for answering OAuth callbacks on localhost*

OAuth is an increasingly popular system for authenticating client software to
Internet services, but it often requires access to a web server. When the
client software is a piece of Open Source software running on a user's laptop
and without any supporting infrastructure, this can present a difficult
obstacle.

This package provides a standard framework for writing OAuth callback handlers
and running them on a local webserver temporarily setup for just that purpose.

## Example

Authenticating to an App.net server:

    >>> from oauthcallback import fetch_access_token
    >>> from oauthcallback.appdotnet import AppDotNetHandler
    >>> token_info = fetch_access_token(AppDotNetHandler,
    ...                                 client_id='foobarbaz',
    ...                                 scope='stream,public_messages')
    >>> token_info['access_token']
    'BigLongAlphanumericString'

At that point, you have the user's access token for use when accessing their
account resources.

## Writing your own handler

Subclass `CallbackHandler` method's:

* `auth_url` returns the URL that the user's web browser with initially open
  with.
* `do_Get` analyzes the callback response request to parse out the access
  token or other relevant data. Call `self.finish_with_result` to stop the web
  server and return the results to the client program.

## License

PythonOAuthCallback is available under the MIT License.
