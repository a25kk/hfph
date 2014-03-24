from five import grok
from plone import api

from Products.statusmessages.interfaces import IStatusMessage
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.publisher.interfaces import IPublishTraverse

from hph.membership import MessageFactory as _


class UserAccount(grok.View):
    grok.context(INavigationRoot)
    grok.implements(IPublishTraverse)
    grok.require('cmf.ManagePortal')
    grok.name('useraccount')

    def update(self):
        self.key = self.traverse_subpath[0]
        self.token = self.traverse_subpath[1]

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
        user = api.user.get(username=self.key)
        stored_token = user.getProperty('token', None)
        if stored_token is None:
            IStatusMessage(self.request).addStatusMessage(
                _(u"No stored acces token found"),
                type='error')
            portal_url = api.portal.get().absolute_url()
            error_url = '{0}/@@useraccount-error'.format(portal_url)
            return self.request.response.redirect(error_url)
        return self.is_equal(stored_token, token)

    def is_equal(a, b):
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
