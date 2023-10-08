# -*- coding: utf-8 -*-
"""Module providing helper views for widget management"""
from zope.interface import alsoProvides

from plone.protect.interfaces import IDisableCSRFProtection

from Products.Five import BrowserView

from ade25.widgets import utils as widget_utils


class SetupPackageWidgets(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        return self.render()

    def render(self):
        idx = self._cleanup_schema()
        return 'Cleaned up {0} objects'.format(idx)

    def _register_content_widgets(self):
        return


class DefaultWidgetsConfiguration(BrowserView):
    """ Generate Widget settings blue print """

    # TODO: this view should probably migrate to the base widget package

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        return self.render()

    def render(self):
        settings = widget_utils.default_widget_configuration()
        return settings
