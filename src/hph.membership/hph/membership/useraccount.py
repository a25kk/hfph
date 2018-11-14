from AccessControl import Unauthorized
from DateTime import DateTime
from five import grok
from plone import api
from zope.component import getMultiAdapter

from Products.CMFPlone.utils import safe_unicode
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.publisher.interfaces import IPublishTraverse

from hph.membership import MessageFactory as _


class UserAccount(grok.View):
    grok.context(INavigationRoot)
    grok.implements(IPublishTraverse)
    grok.require('zope2.View')
    grok.name('useraccount')

    def update(self):
        self.key = self.traverse_subpath[0]
        self.token = self.traverse_subpath[1]
        self.has_valid_token(self.token)
        self.errors = {}
        self.can_set_password = self.has_valid_token(self.token)
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('title')
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            errorIdx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {}
                        error['active'] = True
                        error['msg'] = _(u"This field is required")
                        form_errors[value] = error
                        errorIdx += 1
                    else:
                        error = {}
                        error['active'] = False
                        error['msg'] = form[value]
                        form_errors[value] = error
            if errorIdx > 0:
                self.errors = form_errors
            else:
                self._handle_reset(form)

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def has_valid_token(self, token):
        token = self.traverse_subpath[1]
        user = api.user.get(userid=str(self.key))
        try:
            stored_token = user.getProperty('token', None)
        except AttributeError:
            IStatusMessage(self.request).addStatusMessage(
                _(u"No matching user account found"),
                type='error')
            portal_url = api.portal.get().absolute_url()
            error_url = '{0}/@@useraccount-error'.format(portal_url)
            return self.request.response.redirect(error_url)
        if stored_token is None:
            IStatusMessage(self.request).addStatusMessage(
                _(u"No stored access token found"),
                type='error')
            portal_url = api.portal.get().absolute_url()
            error_url = '{0}/@@useraccount-error'.format(portal_url)
            return self.request.response.redirect(error_url)
        return self.is_equal(stored_token, token)

    def is_equal(self, a, b):
        """ Constant time comparison """
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
        return result == 0

    def user_info(self):
        user = api.user.get(username=self.key)
        info = {}
        info['userid'] = self.key
        info['email'] = user.getProperty('email', '')
        return user

    def _handle_reset(self, data):
        password = str(data.get('password'))
        confirm = str(data.get('confirm'))
        if len(password) < 8:
            errors = {}
            error = {}
            error['active'] = True
            error['msg'] = _(u"This field is required")
            errors['password'] = error
            self.errors = errors
            IStatusMessage(self.request).addStatusMessage(
                _(u"Passwords must consist of at least 8 characters"),
                "error")
            return self.request.response.redirect(self.context.absolute_url())
        if confirm != password:
            IStatusMessage(self.request).addStatusMessage(
                _(u"The entered password and confirmation do not match."),
                "error")
            return self.request.response.redirect(self.context.absolute_url())
        username = str(self.key)
        member = api.user.get(username=username)
        login_name = member.getProperty('email')
        member.setSecurityProfile(password=password)
        update_props = {'enabled': True, 'confirmed': True}
        member.setMemberProperties(mapping=update_props)
        acl = api.portal.get_tool(name='acl_users')
        authenticated = acl.authenticate(login_name,
                                         password,
                                         self.request)
        if authenticated:
            acl.updateCredentials(self.request,
                                  self.request.response,
                                  login_name,
                                  password)

        login_time = member.getProperty('login_time', '2000/01/01')
        base_url = '{0}/ws/{1}'.format(api.portal.get().absolute_url(),
                                       username)
        if not isinstance(login_time, DateTime):
            login_time = DateTime(login_time)
        initial_login = login_time == DateTime('2000/01/01')
        if initial_login:
            mtool = api.portal.get_tool(name='portal_membership')
            mtool.createMemberarea(member_id=username)
            next_url = '{0}?welcome_msg=1'.format(base_url)
        else:
            next_url = base_url
        IStatusMessage(self.request).addStatusMessage(
            _(u"You are now logged in."), "info")
        self.request.response.redirect(next_url)


class UserAccountError(grok.View):
    grok.context(INavigationRoot)
    grok.implements(IPublishTraverse)
    grok.require('zope2.View')
    grok.name('useraccount-error')
