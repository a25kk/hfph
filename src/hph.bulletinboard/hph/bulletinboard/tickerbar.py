from five import grok

from plone.app.layout.viewlets.interfaces import IPortalFooter

from plone.app.layout.navigation.interfaces import INavigationRoot


class TickerViewlet(grok.Viewlet):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalFooter)
    grok.name('hph.bulletinboard.TickerViewlet')
