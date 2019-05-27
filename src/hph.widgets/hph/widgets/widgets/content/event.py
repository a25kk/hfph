# -*- coding: utf-8 -*-
"""Module providing preview cards"""
import uuid as uuid_tool
from Acquisition import aq_inner
from Products.Five import BrowserView
from ade25.base.interfaces import IContentInfoProvider
from plone import api
from plone.i18n.normalizer import IIDNormalizer
from zope.component import queryUtility, getUtility
from zope.schema.interfaces import IVocabularyFactory


class WidgetEventCard(BrowserView):
    """ Basic context content card """

    def __call__(self, widget_data=None, widget_mode="view", **kw):
        self.params = {"widget_mode": widget_mode, "widget_data": widget_data}
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    @property
    def record(self):
        return self.params['widget_data']

    def has_content(self):
        if self.widget_content():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    @staticmethod
    def normalizer():
        return queryUtility(IIDNormalizer)

    def card_subject_classes(self, item):
        context = item
        subjects = context.Subject()
        class_list = [
            "app-card-tag--{0}".format(self.normalizer().normalize(keyword))
            for keyword in subjects
        ]
        return class_list

    def card_css_classes(self, item):
        class_list = self.card_subject_classes(item)
        if class_list:
            return " ".join(class_list)
        else:
            return "app-card-tag--all"

    @staticmethod
    def has_image(context):
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    def event_type_title(self, event_type):
        context = aq_inner(self.context)
        factory = getUtility(IVocabularyFactory, "hph.sitecontent.EventTypes")
        vocabulary = factory(context)
        term = vocabulary.getTerm(event_type)
        return term.title

    def widget_content(self):
        context = aq_inner(self.context)
        widget_data = self.params["widget_data"]
        if "uuid" in widget_data:
            context = api.content.get(UID=widget_data["uuid"])
        details = {
            "title": context.Title(),
            "description": context.Description(),
            "url": context.absolute_url(),
            "timestamp": context.Date,
            "uuid": context.UID(),
            "has_image": self.has_image(context),
            "css_classes": "app-card--{0}".format(
                context.UID()
            ),
            "content_item": context,
            "event_start_date": self.time_stamp(context, context.start),
            "event_end_date": self.time_stamp(context, context.end),
            "event_type": self.event_type_title(
                context.event_type
            ),
            "event_location": context.location
        }
        return details


class WidgetEventTile(BrowserView):
    """ Event teaser box """

    def __call__(self, widget_data=None, widget_mode="view", **kw):
        self.params = {"widget_mode": widget_mode, "widget_data": widget_data}
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    @property
    def record(self):
        return self.params['widget_data']

    def has_content(self):
        if self.widget_content():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    @staticmethod
    def normalizer():
        return queryUtility(IIDNormalizer)

    def card_subject_classes(self, item):
        context = item
        subjects = context.Subject()
        class_list = [
            "app-card-tag--{0}".format(self.normalizer().normalize(keyword))
            for keyword in subjects
        ]
        return class_list

    def card_css_classes(self, item):
        class_list = self.card_subject_classes(item)
        if class_list:
            return " ".join(class_list)
        else:
            return "app-card-tag--all"

    @staticmethod
    def has_image(context):
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    @staticmethod
    def content_snippet(item, text_field):
        content_info_provider = IContentInfoProvider(item)
        text_snippet = content_info_provider.teaser_text(
            text_field, characters=200)
        return text_snippet

    def event_type_title(self, event_type):
        context = aq_inner(self.context)
        factory = getUtility(IVocabularyFactory, "hph.sitecontent.EventTypes")
        vocabulary = factory(context)
        term = vocabulary.getTerm(event_type)
        return term.title

    def widget_content(self):
        context = aq_inner(self.context)
        widget_data = self.params["widget_data"]
        if "uuid" in widget_data:
            context = api.content.get(UID=widget_data["uuid"])
        details = {
            "title": context.Title(),
            "description": context.Description(),
            "snippet": self.content_snippet(context, context.Description()),
            "url": context.absolute_url(),
            "timestamp": context.Date,
            "uuid": context.UID(),
            "has_image": self.has_image(context),
            "css_classes": "app-card--{0}".format(
                context.UID()
            ),
            "content_item": context,
            "event_start_date": self.time_stamp(context, context.start),
            "event_end_date": self.time_stamp(context, context.end),
            "event_type": self.event_type_title(
                context.event_type
            ),
            "event_location": context.location
        }
        return details


class WidgetEventSnippet(BrowserView):
    """ Basic context content snippet """

    def __call__(self, widget_data=None, widget_mode="view", **kw):
        self.params = {"widget_mode": widget_mode, "widget_data": widget_data}
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    @property
    def record(self):
        return self.params['widget_data']

    def has_content(self):
        if self.widget_content():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    @staticmethod
    def normalizer():
        return queryUtility(IIDNormalizer)

    @staticmethod
    def has_image(context):
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    def event_type_title(self, event_type):
        context = aq_inner(self.context)
        factory = getUtility(IVocabularyFactory, "hph.sitecontent.EventTypes")
        vocabulary = factory(context)
        term = vocabulary.getTerm(event_type)
        return term.title

    def widget_content(self):
        context = aq_inner(self.context)
        widget_data = self.params["widget_data"]
        if "uuid" in widget_data:
            context = api.content.get(UID=widget_data["uuid"])
        details = {
            "title": context.Title(),
            "description": context.Description(),
            "url": context.absolute_url(),
            "timestamp": context.Date,
            "uuid": context.UID(),
            "has_image": self.has_image(context),
            "css_classes": "app-card--{0}".format(
                context.UID()
            ),
            "content_item": context,
            "event_start_date": self.time_stamp(context, context.start),
            "event_end_date": self.time_stamp(context, context.end),
            "event_type": self.event_type_title(
                context.event_type
            ),
            "event_location": context.location
        }
        return details
