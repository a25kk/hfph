# -*- coding: utf-8 -*-
# Module providing version specific upgrade steps
from plone import api

import logging

default_profile = 'profile-ploneconf.site:default'
logger = logging.getLogger(__name__)


def upgrade_1003(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    portal = api.portal.get()
    # Update registry settings
    # TODO: implement widget registration
