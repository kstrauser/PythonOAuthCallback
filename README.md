Python OAuth Callback
=====================

*A local webserver for answering OAuth callbacks*

OAuth is an increasingly popular system for authenticating client software to
Internet services, but it often requires access to a web server. When the
client software is Open Source software running on a user's laptop and without
any external supporting infrastructure, this can present a difficult obstacle.

This package provides a standard framework for writing OAuth callback handlers
and running them on a local webserver temporarily set up for just that
purpose.

## Example

Authenticating to an App.net server:

    >>> from oauthcallback.appdotnet import AppDotNetHandler as adn
    >>> token_info = adn.fetch_access_token(
    ...     client_id='XJtBFQwBesZHYE4TGcFwzvfq6D6a7NCa',
    ...     scope='stream,public_messages')
    >>> token_info['access_token']
    'BigLongAlphanumericString'

You now have a token for accessing the user's account resources.

## Writing your own handler

Subclass `CallbackHandler` method's:

* `auth_url` returns the URL that the user's web browser will initially open
  with.

* `do_Get` analyzes the callback request to parse out the access token or
  other relevant data. Call `self.finish_with_result` to stop the web server
  and return the results to the client program.

## License

Python OAuth Callback is available under the MIT License.
