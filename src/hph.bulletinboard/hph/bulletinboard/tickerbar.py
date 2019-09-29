import DateTime
from five import grok
from plone import api

from Acquisition import aq_inner

from hph.bulletinboard.bulletinboard import IBulletinBoard
from zope.interface import Interface
from zope.component import getMultiAdapter

from plone.app.layout.viewlets.interfaces import IPortalFooter

from hph.bulletinboard.bulletin import IBulletin


class TickerViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalFooter)
    grok.name('hph.bulletinboard.TickerViewlet')

    def update(self):
        pstate = getMultiAdapter((self.context, self.request),
                                 name='plone_portal_state')
        self.portal_url = pstate.portal_url
        self.available = self.show_viewlet()

    def show_viewlet(self):
        context = aq_inner(self.context)
        display = False
        if len(self.active_bulletins()) > 0:
            if not IBulletinBoard.providedBy(context):
                display = True
        return display

    def active_bulletins(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        end = DateTime.DateTime() + 0.1
        start = DateTime.DateTime() - 14
        date_range_query = {'query': (start, end), 'range': 'min: max'}
        results = catalog(object_provides=IBulletin.__identifier__,
                          effective=date_range_query,
                          review_state='published')
        return results
