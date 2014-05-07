import json
from Acquisition import aq_inner
from DateTime import DateTime
from five import grok
from plone import api
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.contentlisting.interfaces import IContentListing

from plone.app.event.base import RET_MODE_ACCESSORS
from plone.app.event.base import get_events
from plone.app.event.base import localized_now
from plone.app.event.dx.interfaces import IDXEvent

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
        results = catalog(object_provides=IDXEvent.__identifier__,
                          review_state='published',
                          sort_on='start',
                          sort_order='reverse',
                          sort_limit=3)[:3]
        resultlist = IContentListing(results)
        return resultlist

    def recent_news(self):
        context = aq_inner(self.context)
        portal = api.portal.get()
        catalog = getToolByName(context, 'portal_catalog')
        container = portal['nachrichten']
        results = catalog(object_provides=INewsEntry.__identifier__,
                          path=dict(
                              query='/'.join(container.getPhysicalPath()),
                              depth=1),
                          review_state='published',
                          sort_on='effective',
                          sort_order='reverse',
                          sort_limit=4)[:4]
        return results

    def constructImageTag(self, brain):
        obj = brain.getObject()
        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('image', width=220, height=170)
        data = {}
        if scale is not None:
            data['url'] = scale.url
            data['width'] = scale.width
            data['height'] = scale.height
        return data


class RecentEventsView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('json-eventlist')

    def render(self):
        return json.dumps(self.event_data())

    def event_data(self):
        events = self.events()
        items = list()
        for brain in events:
            item = {}
            item['title'] = brain.title
            item['url'] = brain.url
            item['date'] = self.get_localized_date(brain)
            items.append(item)
        data = {'items': items}
        return data

    def events(self):
        context = aq_inner(self.context)
        portal = api.portal.get()
        container = portal['termine']
        kw = {}
        kw['path'] = dict(query='/'.join(container.getPhysicalPath()),
                          depth=1)
        kw['review_state'] = 'published'
        items = get_events(context, start=localized_now(context),
                           ret_mode=RET_MODE_ACCESSORS,
                           expand=True, limit=3, **kw)
        return items

    def eventitems(self):
        context = aq_inner(self.context)
        portal = api.portal.get()
        container = portal['termine']
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IDXEvent.__identifier__,
                          path=dict(
                              query='/'.join(container.getPhysicalPath()),
                              depth=1),
                          review_state='published',
                          start={'query': DateTime.DateTime(), 'range': 'max'},
                          sort_on='start',
                          sort_limit=3)[:3]
        return results

    def get_localized_date(self, item):
        context = aq_inner(self.context)
        item_start = item.start
        tool = getToolByName(context, 'translation_service')
        return tool.ulocalized_time(item_start,
                                    long_format=False,
                                    time_only=False,
                                    domain='plonelocales',
                                    request=self.request)
