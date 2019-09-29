# -*- coding: utf-8 -*-
"""Module providing custom setup steps"""
import datetime
import json
import logging
import time

import six
from Products.CMFPlone.utils import safe_unicode

from hph.widgets.config import PKG_WIDGETS
from plone import api
from plone.api.exc import InvalidParameterError

logger = logging.getLogger(__name__)


def register_content_widgets(site):
    """Run custom add-on package installation code to add custom
       site specific content widgets

    @param site: Plone site
    """
    content_widgets = PKG_WIDGETS
    widget_settings = api.portal.get_registry_record(
        name="ade25.widgets.widget_settings"
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
        value=safe_unicode(json.dumps(stored_widgets))
    )


def setup_various(context):
    """
    @param context: Products.GenericSetup.context.DirectoryImportContext instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your package or any other
    if context.readDataFile('hph.widgets.marker.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()

    register_content_widgets(portal)
