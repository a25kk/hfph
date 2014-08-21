# -*- coding: UTF-8 -*-
"""Module providing sso token consumer for external discourse installation"""
import base64
import hmac
import hashlib

from five import grok

from plone.app.layout.navigation.interfaces import INavigationRoot

try:  # py3
    from urllib.parse import unquote, urlencode
except ImportError:
    from urllib import unquote, urlencode

from requests.exceptions import HTTPError

DISCOURSE_BASE_URL = 'http://your-discourse-site.com'
DISCOURSE_SSO_SECRET = 'paste_your_secret_here'


class DiscourseError(HTTPError):
    """ A generic error while attempting to communicate with Discourse """


class DiscourseSSOConsumer(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('dc-sso-consumner')

    def discourse_sso_view(self):
        payload = self.request.get('sso')
        signature = self.request.get('sig')
        try:
            nonce = sso_validate(payload, signature, DISCOURSE_SSO_SECRET)
        except DiscourseError as e:
            return 'HTTP400 Error {}'.format(e)  # Todo: implement handler

        url = sso_redirect_url(nonce,
                               DISCOURSE_SSO_SECRET,
                               self.request.user.email,
                               self.request.user.id,
                               self.request.user.username)
        return self.request.response.redirect(
            'http://discuss.example.com' + url)


def sso_validate(payload, signature, secret):
    """
        payload: provided by Discourse HTTP call to your SSO endpoint as sso
                 GET param
        signature: provided by Discourse HTTP call to your SSO endpoint as sig
                   GET param
        secret: the secret key you entered into Discourse sso secret

        return value: The nonce used by discourse to validate the redirect URL
    """
    if None in [payload, signature]:
        raise DiscourseError('No SSO payload or signature.')

    if not secret:
        raise DiscourseError('Invalid secret..')

    payload = unquote(payload)
    if not payload:
        raise DiscourseError('Invalid payload..')

    decoded = base64.decodestring(payload)
    if 'nonce' not in decoded:
        raise DiscourseError('Invalid payload..')

    h = hmac.new(secret, payload, digestmod=hashlib.sha256)
    this_signature = h.hexdigest()

    if this_signature != signature:
        raise DiscourseError('Payload does not match signature.')

    nonce = decoded.split('=')[1]

    return nonce


def sso_redirect_url(nonce, secret, email, external_id, username, **kwargs):
    """
        nonce: returned by sso_validate()
        secret: the secret key you entered into Discourse sso secret
        user_email: email address of the user who logged in
        user_id: the internal id of the logged in user
        user_username: username of the logged in user

        return value: URL to redirect users back to discourse, now logged in as
        user_username
    """
    kwargs.update({
        'nonce': nonce,
        'email': email,
        'external_id': external_id,
        'username': username
    })

    return_payload = base64.encodestring(urlencode(kwargs))
    h = hmac.new(secret, return_payload, digestmod=hashlib.sha256)
    query_string = urlencode({'sso': return_payload, 'sig': h.hexdigest()})

    return '/session/sso_login?%s' % query_string
