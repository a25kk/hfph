from five import grok
from zope.component import getUtility

from plone.app.layout.navigation.interfaces import INavigationRoot
from hph.membership.tool import IHPHMemberTool


class MemberListing(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('member-listing')

    def external_members(self):
        tool = getUtility(IHPHMemberTool)
        records = tool.get()
        return records
