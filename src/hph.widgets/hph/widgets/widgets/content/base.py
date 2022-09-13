# -*- coding: utf-8 -*-
"""Module providing preview cards"""
import uuid as uuid_tool

from zope.component import queryUtility

from plone import api
from plone.i18n.normalizer import IIDNormalizer

from Acquisition import aq_inner
from Products.Five import BrowserView


class WidgetContentCard(BrowserView):
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

    def widget_content(self):
        context = aq_inner(self.context)
        widget_data = self.params["widget_data"]
        if widget_data and "uuid" in widget_data:
            context = api.content.get(UID=widget_data["uuid"])
        details = {
            "title": context.Title(),
            "description": context.Description(),
            "url": context.absolute_url(),
            "timestamp": context.Date,
            "uuid": context.UID(),
            "has_image": self.has_image(context),
            "css_classes": "app-card--{0} {1}".format(
                context.UID(), self.card_css_classes(context)
            ),
            "content_item": context,
        }
        return details


class WidgetContentSnippet(BrowserView):
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
            "css_classes": "app-card--{0} {1}".format(
                context.UID(), self.card_css_classes(context)
            ),
            "content_item": context,
        }
        return details
