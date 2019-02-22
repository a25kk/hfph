# -*- coding: utf-8 -*-
"""Module providing site widget"""
import uuid as uuid_tool
from Products.Five import BrowserView


class WidgetTeaserNews(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='teaser-news',
                 widget_type='teaser-news',
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
        if self.widget_text_block():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_text_block(self):
        try:
            content = self.record['data']['content']['text_column_0']
        except (KeyError, TypeError):
            content = None
        return content
