from five import grok
from zope.interface import Interface
from zope.component import getMultiAdapter
from plone.app.layout.viewlets.interfaces import IPortalFooter

from plone.app.layout.navigation.interfaces import INavigationRoot


class TickerViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalFooter)
    grok.name('hph.bulletinboard.TickerViewlet')

    def update(self):
        pstate = getMultiAdapter((self.context, self.request),
                    name='plone_portal_state')
        self.portal_url = pstate.portal_url
