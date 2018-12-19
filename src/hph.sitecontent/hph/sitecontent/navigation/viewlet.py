# -*- coding: utf-8 -*-
"""Module providing custom navigation strategy"""
from plone import api
from plone.app.layout.viewlets import ViewletBase


class SiteNavigationViewlet(ViewletBase):
    """ Context aware responsive navigation viewlet """

    @staticmethod
    def section_types():
        section_types = list()
        settings = api.portal.get_registry_record(
            name='ade25.base.listed_content_types'
        )
        if settings:
            section_types = settings
        return section_types

    def available(self):
        if self.section_types():
            return True
        return False
