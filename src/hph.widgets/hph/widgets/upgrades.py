# -*- coding: utf-8 -*-
# Module providing version specific upgrade steps
import logging
import datetime
import json
import time

import six

from hph.widgets.config import PKG_WIDGETS
from plone import api

default_profile = 'profile-hph.widgets:default'
logger = logging.getLogger(__name__)


def register_content_widgets(site):
    """Run custom add-on package installation code to add custom
       site specific content widgets

    @param site: Plone site
    """
    content_widgets = PKG_WIDGETS
    widget_settings = api.portal.get_registry_record(
        name='ade25.widgets.widget_settings'
    )
    stored_widgets = json.loads(widget_settings)
    records = stored_widgets['items']
    for content_widget, widget_data in content_widgets.items():
        if content_widget not in records.keys():
            records[content_widget] = widget_data
    stored_widgets["items"] = records
    stored_widgets["timestamp"] = six.text_type(int(time.time())),
    stored_widgets["updated"] = datetime.datetime.now().isoformat(),
    api.portal.set_registry_record(
        name='ade25.widgets.widget_settings',
        value=json.dumps(stored_widgets)
    )


def upgrade_1002(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    portal = api.portal.get()
    # Register project specific content widgets
    register_content_widgets(portal)
