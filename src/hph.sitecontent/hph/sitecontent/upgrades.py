# -*- coding: utf-8 -*-
# Module providing version specific upgrade steps
from plone import api

import logging

default_profile = 'profile-hph.sitecontent:default'
logger = logging.getLogger(__name__)


def add_exclude_from_nav_index():
    """Add exclude_from_nav index to the portal_catalog.
    """
    index_name = 'exclude_from_nav'
    meta_type = 'BooleanIndex'
    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()
    indexables = []
    if index_name not in indexes:
        catalog.addIndex(index_name, meta_type)
        indexables.append(index_name)
        logger.info('Added %s for field %s.', meta_type, index_name)
    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def add_exclude_from_footer_nav_index():
    """Add exclude_from_nav index to the portal_catalog.
    """
    index_name = 'exclude_from_toc'
    meta_type = 'BooleanIndex'
    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()
    indexables = []
    if index_name not in indexes:
        catalog.addIndex(index_name, meta_type)
        indexables.append(index_name)
        logger.info('Added %s for field %s.', meta_type, index_name)
    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def upgrade_1003(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    portal = api.portal.get()
    # Create a folder 'Quick-Links' if needed
    if 'quick-links' not in portal:
        quick_links_folder = api.content.create(
            container=portal,
            type='Folder',
            id='quick-links',
            title=u'Quick-Links')
    else:
        quick_links_folder = portal['quick-links']
    if 'quick-link-example' not in quick_links_folder:
        api.content.create(
            container=quick_links_folder,
            type='Link',
            id='quick-link-example',
            title=u'Quick-Link Example',
            url=portal.absolute_url()
        )
    # Setup exclude from navigation index if note already present
    add_exclude_from_nav_index()

    # Update registry settings
    # TODO: implement widget registration


def upgrade_1004(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')


def upgrade_1005(setup):
    setup.runImportStepFromProfile(default_profile, 'catalog')
    add_exclude_from_footer_nav_index()
