import json
import DateTime
from five import grok
from Acquisition import aq_inner

from plone import api
from plone.directives import dexterity, form

from Products.CMFCore.utils import getToolByName

from plone.app.contentlisting.interfaces import IContentListing
from hph.bulletinboard.bulletin import IBulletin

from hph.bulletinboard import MessageFactory as _


class IBulletinBoard(form.Schema):
    """
    A bulletin board holding announcements
    """


class BulletinBoard(dexterity.Container):
    grok.implements(IBulletinBoard)


class View(grok.View):
    grok.context(IBulletinBoard)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_bulletins = len(self.active_bulletins()) > 0

    def active_bulletins(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        end = DateTime.DateTime() + 0.1
        start = DateTime.DateTime() - 14
        date_range_query = {'query': (start, end), 'range': 'min: max'}
        results = catalog(object_provides=IBulletin.__identifier__,
                          effective=date_range_query,
                          review_state='published')
        return IContentListing(results)


class BulletinView(grok.View):
    grok.context(IBulletinBoard)
    grok.require('zope2.View')
    grok.name('bulletins')

    def update(self):
        self.data = self.active_bulletins()

    def render(self):
        return json.dumps(self._jsondata())

    def _jsondata(self):
        context = aq_inner(self.context)
        bulletins = self.active_bulletins()
        items = list()
        for brain in bulletins:
            item = {}
            item['title'] = brain.Title
            item['url'] = context.absolute_url()
            items.append(item)
        data = {'items': items}
        return data

    def active_bulletins(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        end = DateTime.DateTime() + 0.1
        start = DateTime.DateTime() - 14
        date_range_query = {'query': (start, end), 'range': 'min: max'}
        results = catalog(object_provides=IBulletin.__identifier__,
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          effective=date_range_query,
                          review_state='published')
        return results
