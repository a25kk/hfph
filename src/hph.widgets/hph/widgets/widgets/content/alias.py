# -*- coding: utf-8 -*-
"""Module providing base widget"""
from __future__ import print_function
import uuid as uuid_tool

from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.Five import BrowserView
from ade25.widgets.interfaces import IContentWidgets
from plone import api
from plone.app.contenttypes.utils import replace_link_variables_by_paths


class WidgetHPHContentAlias(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='hph-content-alias',
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
        if self.widget_content_record():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def related_content_page(self):
        """Returns a list of brains of related items."""
        results = []
        catalog = api.portal.get_tool('portal_catalog')
        record = self.widget_content_record()
        if record:
            for rel in record['alias']:
                if rel.isBroken():
                    # skip broken relationsY
                    continue
                # query by path so we don't have to wake up any objects
                try:
                    brains = catalog(path={'query': rel.to_path, 'depth': 0})
                    results.append(brains[0])
                except (Unauthorized, IndexError):
                    print((rel.from_object.Title))
                    pass
        return results

    def has_related_content_page(self):
        return len(self.related_content_page()) > 0

    def widget_content_record(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        content = storage.read_widget(self.widget_uid())
        return content

    @staticmethod
    def resolve_alias(content_uuid):
        content_item = api.content.get(UID=content_uuid)
        return content_item.text

    def widget_content(self):
        widget_content = self.widget_content_record()
        data = {
            'text': self.resolve_alias(widget_content['alias']),
            'public': widget_content['is_public']
        }
        return data

    def get_link_action(self, link):
        context = aq_inner(self.context)
        link_action = replace_link_variables_by_paths(context, link)
        return link_action
