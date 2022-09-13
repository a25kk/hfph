# from five import grok
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
