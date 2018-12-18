# -*- coding: utf-8 -*-
"""Module providing custom navigation strategy"""
from Acquisition import aq_inner
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from Products.Five import BrowserView
from plone import api
from plone.app.layout.navigation.navtree import buildFolderTree
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

    def build_nav_tree(self, root, query):
        """
        Create a list of portal_catalog queried items

        @param root: Content item which acts as a navigation root

        @param query: Dictionary of portal_catalog query parameters

        @return: Dictionary of navigation tree
        """
        context = aq_inner(self.context)
        # Navigation tree base portal_catalog query parameters
        applied_query = {
            'path': '/'.join(root.getPhysicalPath()),
            'sort_on': 'getObjPositionInParent',
            'review_state': 'published'
        }
        # Apply caller's filters
        applied_query.update(query)
        # - use navigation portlet strategy as base
        strategy = DefaultNavtreeStrategy(root)
        strategy.rootPath = '/'.join(root.getPhysicalPath())
        strategy.showAllParents = False
        strategy.bottomLevel = 999
        # This will yield out tree of nested dicts of
        # item brains with retrofitted navigational data
        tree = buildFolderTree(context,
                               obj=context,
                               query=query,
                               strategy=strategy)
        return tree

    def _navigation_cachekey(method, self):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type=self.section_types)
        cache_key = sum([int(i.modified) for i in brains])
        return cache_key

    # @ram.cache(_navigation_cachekey)
    def nav_items(self):
        portal = api.portal.get()
        navigation_types = ['Folder', ]
        settings = api.portal.get_registry_record(
            name='ade25.base.listed_content_types'
        )
        if settings:
            navigation_types = settings
        nav_tree_query = {
            'portal_type': navigation_types
        }
        brains = self.build_nav_tree(
            portal,
            query=nav_tree_query
        )
        return brains
