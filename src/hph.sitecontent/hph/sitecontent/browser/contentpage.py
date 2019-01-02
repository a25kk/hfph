# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api

from hph.sitecontent.contentpage import IContentPage


class ContentPageView(BrowserView):
    """ Folderish content page default view """

    def has_leadimage(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def has_contacts(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.relatedContacts
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def display_gallery(self):
        context = aq_inner(self.context)
        try:
            display = context.displayGallery
        except AttributeError:
            display = None
        if display is not None:
            return display
        return False

    def display_cards(self):
        context = aq_inner(self.context)
        try:
            display = context.displayPreviewCards
        except AttributeError:
            display = None
        if display is not None:
            return display
        return False

    def contained_pages(self):
        context = aq_inner(self.context)
        items = api.content.find(
            context=context,
            depth=1,
            object_provides=IContentPage,
            sort_on='getObjPositionInParent'
        )
        return items

    def has_contained_pages(self):
        return len(self.contained_pages()) > 0

    def rendered_card(self, uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse('@@card-view')()
        return template

    def rendered_gallery(self):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@gallery-view')()
        return template

    def content_widget(self, widget='base'):
        context = aq_inner(self.context)
        requested_widget = widget
        widget_view_name = '@@content-widget-{0}'.format(
            requested_widget
        )
        template = context.restrictedTraverse(widget_view_name)(
            widget_type=requested_widget,
            identifier=requested_widget
        )
        return template
