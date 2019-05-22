# -*- coding: utf-8 -*-
"""Module providing helper views for widget management"""
from Products.Five import BrowserView
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class SetupPackageWidgets(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        return self.render()

    def render(self):
        idx = self._cleanup_schema()
        return 'Cleaned up {0} objects'.format(idx)

    def _register_content_widgets(self):
        return
