# -*- coding: utf-8 -*-
"""Module providing news browser views"""
from Products.Five import BrowserView
from hph.sitecontent.newsentry import INewsEntry
from plone import api


class NewsListView(BrowserView):
    """Provide listing of contained news items content"""

    def __call__(self):
        self.has_content = len(self.contained_news_items()) > 0
        return self.render()

    def render(self):
        return self.index()

    def news_items(self):
        results = []
        # brains = api.content.find(context=self.context, portal_type='talk')
        brains = self.contained_news_items()
        for brain in brains:
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'timestamp': brain.Date,
                'uuid': brain.UID,
                'item_object': brain.getObject()
            })
        return results

    def contained_news_items(self):
        items = api.content.find(
            context=self.context,
            object_provides=INewsEntry.__identifier__,
            review_state='published',
            sort_on='Date',
            sort_order='reverse'
        )
        return items

    @staticmethod
    def rendered_news_entry_card(uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse('@@news-entry-card')()
        return template


class NewsEntryCard(BrowserView):
    """ Embeddable card view for news entries"""

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()
