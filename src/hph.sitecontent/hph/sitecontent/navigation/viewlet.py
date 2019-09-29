# -*- coding: utf-8 -*-
"""Module providing custom navigation strategy"""
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from hph.sitecontent import config as hph_config
from hph.sitecontent.browser.controlpanel import IHphBaseControlPanelNavigation


class SiteNavigationViewlet(ViewletBase):
    """ Context aware responsive navigation viewlet """

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IHphBaseControlPanelNavigation,
            prefix='hph.base')
        return settings

    def section_types(self):
        section_types = list()
        try:
            configured_types = self.settings.listed_content_types
            if configured_types:
                section_types = configured_types
        except KeyError:
            pass
        return section_types

    @property
    def nav_tree_element_close(self):
        try:
            navigation_close = self.settings.navigation_element_close
        except (AttributeError, KeyError):
            navigation_close = hph_config.navigation_elements(action='close')
        return navigation_close

    def available(self):
        if self.section_types():
            return True
        return False


class SiteTOCViewlet(ViewletBase):
    """ Context aware responsive toc viewlet """

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IHphBaseControlPanelNavigation,
            prefix='hph.base')
        return settings

    def section_types(self):
        section_types = list()
        try:
            configured_types = self.settings.listed_content_types
            if configured_types:
                section_types = configured_types
            return section_types
        except KeyError:
            return section_types

    def available(self):
        if self.section_types():
            return True
        return False
