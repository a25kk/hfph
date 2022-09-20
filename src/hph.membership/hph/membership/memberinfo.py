# from five import grok
from zope.component import getUtility

from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.publisher.interfaces import IPublishTraverse

from hph.membership.tool import IHPHMemberTool


class MemberListing(object):
    # context(INavigationRoot)
    # require('cmf.ManagePortal')
    # name('member-listing')

    def external_members(self):
        tool = getUtility(IHPHMemberTool)
        records = tool.get()
        return records


class EnableUserAccount(object):
    # context(INavigationRoot)
    # implements(IPublishTraverse)
    # require('cmf.ManagePortal')
    # name('enable-user-account')

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
