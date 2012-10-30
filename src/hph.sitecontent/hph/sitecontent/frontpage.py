from Acquisition import aq_inner
from five import grok
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.contentlisting.interfaces import IContentListing

from hph.sitecontent.eventitem import IEventItem
from hph.sitecontent.newsentry import INewsEntry


class FrontpageView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('frontpage-view')

    def update(self):
        self.has_events = len(self.eventitems()) > 0
        self.has_news = len(self.recent_news()) > 0

    def eventitems(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IEventItem.__identifier__,
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist

    def newsitems(self):
        news = self.recent_news()
        items = []
        for x in news:
            item = {}
            item['title'] = x.Title
            item['description'] = x.Description
            item['url'] = x.getURL,
            item['image_tag'] = self.constructImageTag(x)
            items.append(item)
        return items

    def recent_news(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=INewsEntry.__identifier__,
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist

    def constructImageTag(self, item):
        obj = item.getObject()
        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('image', width=200, height=200)
        item = {}
        import pdb; pdb.set_trace( )
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        return item
