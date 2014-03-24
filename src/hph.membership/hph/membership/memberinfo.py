from five import grok
from plone import api
from zope.component import getUtility

from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.publisher.interfaces import IPublishTraverse

from hph.membership.tool import IHPHMemberTool


class MemberListing(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('member-listing')

    def external_members(self):
        tool = getUtility(IHPHMemberTool)
        records = tool.get()
        return records


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
            return  # Todo: add handler for invalid request
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


class EnableUserAccount(grok.View):
    grok.context(INavigationRoot)
    grok.implements(IPublishTraverse)
    grok.require('cmf.ManagePortal')
    grok.name('enable-user-account')

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
