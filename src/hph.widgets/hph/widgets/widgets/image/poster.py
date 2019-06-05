# -*- coding: utf-8 -*-
"""Module providing base widget"""
import uuid as uuid_tool

from Acquisition import aq_inner
from Products.Five import BrowserView
from ade25.widgets.interfaces import IContentWidgets
from plone import api


class WidgetImagePoster(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='image-poster',
                 widget_type='base',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
        }
        return self.render()

    def render(self):
        return self.index()

    @property
    def edit_mode(self):
        if self.params['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.params['widget_data']

    def has_content(self):
        if self.widget_image_cover():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def has_lead_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    @staticmethod
    def image_tag(image_uid):
        image = api.content.get(UID=image_uid)
        figure = image.restrictedTraverse('@@figure')(
            image_field_name='image',
            caption_field_name='image_caption',
            scale='ratio-4:3',
            aspect_ratio='4/3',
            lqip=True,
            lazy_load=True
        )
        return figure

    def widget_image_cover(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        content = storage.read_widget(self.widget_uid())
        return content

    def widget_content(self):
        widget_content = self.widget_image_cover()
        data = {
            'image': self.image_tag(widget_content['image']),
            'headline': widget_content['title'],
            'text': widget_content['description'],
            'public': widget_content['is_public']
        }
        return data
