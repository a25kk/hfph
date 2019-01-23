# -*- coding: utf-8 -*-
# Module providing version specific upgrade steps
from plone import api

import logging

default_profile = 'profile-hph.sitecontent:default'
logger = logging.getLogger(__name__)


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
    if 'quick-link-example' not in quick-quick_links_folder:
        api.content.create(
            container=quick_links_folder,
            type='Link',
            id='quick-link-example',
            title=u'Quick-Link Example',
            url=portal.absolute_url()
        )

    # Update registry settings
    # TODO: implement widget registration
