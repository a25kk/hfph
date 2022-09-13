# -*- coding: utf-8 -*-
"""Module providing custom navigation strategy"""
from plone import api
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from plone.app.layout.viewlets import ViewletBase

from Acquisition import aq_inner


class QuickLinksViewlet(ViewletBase):
    """ Context aware quick link navigation viewlet """

    @staticmethod
    def quick_links_storage():
        portal = api.portal.get()
        try:
            quick_links_folder = portal['quick-links']
            return quick_links_folder
        except KeyError:
            return None

    def get_link_action(self, item):
        context = aq_inner(self.context)
        link = item.remoteUrl
        link_action = replace_link_variables_by_paths(context, link)
        return link_action

    def quick_links(self):
        configured_links = api.content.find(
            context=self.quick_links_storage(),
            portal_type="Link",
            depth=2
        )
        quick_links = []
        for link in configured_links:
            link_details = {
                'name': link.Title,
                'link': self.get_link_action(link.getObject())
            }
            quick_links.append(link_details)
        return quick_links

    def available(self):
        if self.quick_links_storage():
            return True
        return False
