import json
import DateTime
# # from five import grok
from Acquisition import aq_inner

from plone import api
from plone.autoform.form import AutoExtensibleForm


from Products.CMFCore.utils import getToolByName
from plone.dexterity.content import Container
from plone.supermodel import model

from plone.app.contentlisting.interfaces import IContentListing
from zope.interface import implementer

from hph.bulletinboard.bulletin import IBulletin

from hph.bulletinboard import MessageFactory as _


class IBulletinBoard(model.Schema):
    """
    A bulletin board holding announcements
    """


@implementer(IBulletinBoard)
class BulletinBoard(Container):
    pass


class View(object):

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


class BulletinView(object):


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
