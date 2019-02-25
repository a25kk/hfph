# -*- coding: utf-8 -*-
"""Module providing event views and listings"""
from Acquisition import aq_inner
from Products.Five import BrowserView
from ade25.base.interfaces import IContentInfoProvider
from hph.sitecontent.eventitem import IEventItem
from hph.sitecontent.vocabulary import EventCategoryVocabulary
from hph.sitecontent import MessageFactory as _
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class EventListView(BrowserView):
    """Provide listing of contained event content"""

    def __call__(self):
        self.has_content = len(self.contained_items()) > 0
        return self.render()

    def render(self):
        return self.index()

    def event_type_title(self, event_type):
        context = aq_inner(self.context)
        factory = getUtility(IVocabularyFactory, "hph.sitecontent.EventTypes")
        vocabulary = factory(context)
        term = vocabulary.getTerm(event_type)
        return term.title

    def time_stamp(self, date_time):
        context = aq_inner(self.context)
        content_info_provider = IContentInfoProvider(context)
        return content_info_provider.time_stamp(date_time)

    def contained_items(self):
        items = api.content.find(
            context=self.context,
            object_provides=IEventItem.__identifier__,
            review_state="published",
            sort_on="Start",
            sort_order="reverse",
        )
        return items

    def event_items(self):
        results = []
        # brains = api.content.find(context=self.context, portal_type='talk')
        brains = self.contained_items()
        for brain in brains:
            results.append(
                {
                    "title": brain.Title,
                    "description": brain.Description,
                    "url": brain.getURL(),
                    "timestamp": brain.Date,
                    "uuid": brain.UID,
                    "event_start_date": self.time_stamp(brain.start),
                    "event_end_date": self.time_stamp(brain.end),
                    "event_type": self.event_type_title(
                        brain.getObject().event_type
                    ),
                    "item_object": brain.getObject(),
                }
            )
        return results

    @staticmethod
    def rendered_news_entry_card(uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse("@@news-entry-card")()
        return template


class EventItemView(BrowserView):
    """ news item"""

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def has_lead_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def time_stamp(self, date_time):
        context = aq_inner(self.context)
        content_info_provider = IContentInfoProvider(context)
        return content_info_provider.time_stamp(date_time)

    def event_type_title(self):
        context = aq_inner(self.context)
        event_type = getattr(context, "event_type", _("Event"))
        factory = getUtility(IVocabularyFactory, "hph.sitecontent.EventTypes")
        vocabulary = factory(context)
        term = vocabulary.getTerm(event_type)
        return term.title
