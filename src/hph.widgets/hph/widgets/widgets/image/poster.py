# -*- coding: utf-8 -*-
"""Module providing base widget"""
import uuid as uuid_tool

from Acquisition import aq_inner
from Products.Five import BrowserView
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
            scale='4:3',
            aspect_ratio='4/3',
            lqip=True,
            lazy_load=True
        )
        return figure

    def widget_image_cover(self):
        try:
            content = self.record['data']['content']['poster_image']
        except (KeyError, TypeError):
            content = None
        return content

    def widget_content(self):
        image_uid = self.widget_image_cover()
        data = {
            'image': self.image_tag(image_uid),
            'headline': self.record['data']['content']['title'],
            'text': self.record['data']['content']['text'],
            'link': self.record['data']['content']['link']
        }
        return data
