# -*- coding: utf-8 -*-
"""Module providing event views and listings"""
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from plone import api

import DateTime
from Acquisition import aq_inner
from Products.Five import BrowserView

from ade25.base.interfaces import IContentInfoProvider
from hph.sitecontent import MessageFactory as _
from hph.sitecontent.eventitem import IEventItem
from hph.sitecontent.vocabulary import EventCategoryVocabulary


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
        try:
            content_info_provider = IContentInfoProvider(context)
        except TypeError:
            # Since we reuse the view standalone on the site root which is not
            # content by design we need to adopt the interface to a content item
            # in order to get hold of the tool
            content_info_provider = IContentInfoProvider(context['startseite'])
        return content_info_provider.time_stamp(date_time)

    def contained_items(self):
        items = api.content.find(
            context=self.context,
            object_provides=IEventItem.__identifier__,
            review_state="published",
            end={'query': DateTime.DateTime(), 'range': 'min'},
            sort_on="start",
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
                    "timestamp": brain.start,
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

    def is_full_day_event(self):
        context = aq_inner(self.context)
        return getattr(context, 'full_day', False)

    def is_open_end_event(self):
        context = aq_inner(self.context)
        return getattr(context, 'open_end', False)

    def show_event_end_date(self):
        if not self.is_full_day_event() and not self.is_open_end_event():
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
