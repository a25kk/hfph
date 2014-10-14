# -*- coding: UTF-8 -*-
"""Module providing sso token consumer for external discourse installation"""

import base64
import hmac
import hashlib
import urlparse

try:  # py3
    from urllib.parse import unquote, urlencode
except ImportError:
    from urllib import unquote, urlencode

from requests.exceptions import HTTPError

from DateTime import DateTime
from five import grok
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.directives import form
from zope import schema
from zope.interface import Interface
from z3c.form import button
from z3c.form.interfaces import HIDDEN_MODE

from hph.membership import MessageFactory as _


class IDiscourseSigninForm(Interface):
    """ Login form schema """

    ac_name = schema.TextLine(
        title=_(u'Login Name'),
        required=True,
    )
    ac_password = schema.Password(
        title=_(u'Password'),
        required=True,
    )
    sso = schema.TextLine(
        title=_(u'SSO payload'),
        required=False,
    )
    sig = schema.TextLine(
        title=_(u'SSO Signature'),
        required=False,
    )


class DiscourseSigninForm(form.SchemaForm):
    """ Implementation of the login form """
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('discourse-signin')

    schema = IDiscourseSigninForm

    id = "LoginForm"
    label = _(u"Log in")
    description = _(u"Please enter your credentials to verify SSO login")

    ignoreContext = True

    prefix = ""

    def update(self):
        self.request.set('disable_border', True)
        super(DiscourseSigninForm, self).update()

    def updateActions(self):
        super(DiscourseSigninForm, self).updateActions()
        self.actions['signin'].addClass("btn btn-primary")

    def updateWidgets(self):
        try:
            auth = self.context.acl_users.credentials_cookie_auth
        except:
            try:
                auth = self.context.cookie_authentication
            except:
                auth = None
        if auth:
            self.fields['ac_name'].__name__ = auth.get('name_cookie',
                                                       '__ac_name')
            self.fields['ac_password'].__name__ = auth.get('pw_cookie',
                                                           '__ac_password')
        else:
            self.fields['ac_name'].__name__ = '__ac_name'
            self.fields['ac_password'].__name__ = '__ac_password'

        super(DiscourseSigninForm, self).updateWidgets(prefix="")
        self.widgets['sso'].mode = HIDDEN_MODE
        self.widgets['sig'].mode = HIDDEN_MODE

    @button.buttonAndHandler(_('Log in'), name='signin')
    def handleLogin(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        membership_tool = api.portal.get_tool(name='portal_membership')
        if membership_tool.isAnonymousUser():
            self.request.response.expireCookie('__ac', path='/')
            email_login = api.portal.get_tool(name='portal_properties') \
                .site_properties.getProperty('use_email_as_login')
            if email_login:
                api.portal.show_message(
                    _(u'Login failed. Both email address and password are case'
                      u' sensitive, check that caps lock is not enabled.'),
                    self.request,
                    type='error')
            else:
                api.portal.show_message(
                    _(u'Login failed. Both login name and password are case '
                      u'sensitive, check that caps lock is not enabled.'),
                    self.request,
                    type='error')
            return

        member = membership_tool.getAuthenticatedMember()
        login_time = member.getProperty('login_time', '2000/01/01')
        if not isinstance(login_time, DateTime):
            login_time = DateTime(login_time)

        membership_tool.loginUser(self.request)

        api.portal.show_message(
            _(u"You are now logged in."), self.request, type="info")
        url = '{0}/@@discourse-sso?sso={1}&sig={2}'.format(
            self.context.portal_url(), data['sso'], data['sig'])
        self.request.response.redirect(url)


class DiscourseError(HTTPError):
    """ A generic error while attempting to communicate with Discourse """


class DiscourseSSOHandler(grok.View):
    """ Discourse SSO endpoint that handles user login
        and secret validation and digestion
    """
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('discourse-sso')

    def render(self):
        portal_url = api.portal.get().absolute_url()
        actual_url = self.request.get('ACTUAL_URL')
        if not actual_url.startswith('http://'):
            msg = _(u"The Discourse SSO endpoint can only be accessed via "
                    u"SSL since we do not support transfer of authentication "
                    u"tokens via unencrypted connections.")
            api.portal.show_message(msg, self.request, type='info')
            error_page = '{0}/@@discourse-sso-error'.format(portal_url)
            return self.request.response.redirect(error_page)
        discourse_url = self.get_stored_records(token='discourse_url')
        sso_secret = self.get_stored_records(token='discourse_sso_secret')
        if not discourse_url or not sso_secret:
            msg = _(u"The Discourse SSO endpoint has not been configured yet")
            api.portal.show_message(msg, self.request, type='info')
            error_page = '{0}/@@discourse-sso-error'.format(portal_url)
            return self.request.response.redirect(error_page)
        payload = self.request.get('sso')
        signature = self.request.get('sig')
        if payload is None:
            msg = _(u"Required parameters for SSO credential verification are "
                    u"missing in the request")
            api.portal.show_message(msg, self.request, type='error')
            error_page = '{0}/@@discourse-sso-error'.format(portal_url)
            return self.request.response.redirect(error_page)
        discourse_url = self.get_stored_records(token='discourse_url')
        sso_secret = self.get_stored_records(token='discourse_sso_secret')
        if api.user.is_anonymous():
            url = '{0}/@@discourse-signin?sso={1}&sig={2}'.format(portal_url,
                                                                  payload,
                                                                  signature)
            return self.request.response.redirect(url)

        try:
            nonce = self.sso_validate(payload,
                                      signature,
                                      str(sso_secret))
        except DiscourseError as e:
            return 'HTTP400 Error {}'.format(e)  # Todo: implement handler
        user = api.user.get_current()
        url = self.sso_redirect_url(nonce,
                                    sso_secret,
                                    user.getProperty('email'),
                                    user.getId(),
                                    user.getProperty('fullname'))
        return self.request.response.redirect(discourse_url + url)

    def is_equal(self, a, b):
        """ Constant time comparison """
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
        return result == 0

    def get_stored_records(self, token):
        key_base = 'hph.membership.interfaces.IHPHMembershipSettings'
        key = key_base + '.' + token
        return api.portal.get_registry_record(key)

    def sso_validate(self, payload, signature, secret):
        """
            payload: provided by Discourse HTTP call as sso GET param
            signature: provided by Discourse HTTP call as sig GET param
            secret: the secret key you entered into Discourse sso secret

            return value: The nonce intended to validate the redirect URL
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

        if not self.is_equal(this_signature, signature):
            raise DiscourseError('Payload does not match signature.')

        # nonce = decoded.split('=')[1]

        sso = urlparse.parse_qs(payload.decode('base64'))
        nonce = sso['nonce'][0]

        return nonce

    def sso_redirect_url(self,
                         nonce,
                         secret,
                         email,
                         external_id,
                         username,
                         **kwargs):
        """
            nonce: returned by sso_validate()
            secret: the secret key you entered into Discourse sso secret
            user_email: email address of the user who logged in
            user_id: the internal id of the logged in user
            user_username: username of the logged in user (an email address)

            return value:
            URL to redirect users back to discourse, now logged in as username
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


class DiscourseSSOError(grok.View):
    """ Discourse SSO endpoint error page """
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('discourse-sso-error')
