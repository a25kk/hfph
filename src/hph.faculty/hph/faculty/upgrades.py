# -*- coding: utf-8 -*-
# Module providing version specific upgrade steps
from plone import api

import logging

default_profile = 'profile-hph.faculty:default'
logger = logging.getLogger(__name__)


def upgrade_1001(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    setup.runImportStepFromProfile(default_profile, 'portlets')
