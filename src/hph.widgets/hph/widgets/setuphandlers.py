# -*- coding: utf-8 -*-
"""Module providing custom setup steps"""
import json

from plone import api


def register_content_widgets(site):
    """Run custom add-on package installation code to add custom
       site specific content widgets

    @param site: Plone site
    """
    content_widgets = [
        'teaser-news',
        'hph-image-poster'
    ]
    widget_settings = api.portal.get_registry_record(
        name='ade25.widgets.widget_settings'
    )
    stored_widgets = json.loads(widget_settings)
    for widget_type in content_widgets:
        if widget_type not in stored_widgets:
            # Generate default settings via widgets tool
            stored_widgets.append(widget_type)
    api.portal.set_registry_record(
        name='ade25.widgets.widget_settings',
        value=json.dumps(stored_widgets)
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
