# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from plone import api

from hph.widgets.testing import IntegrationTestCase


class TestInstall(IntegrationTestCase):
    """Test installation of hph.widgets into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if hph.widgets is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('hph.widgets'))

    def test_uninstall(self):
        """Test if hph.widgets is cleanly uninstalled."""
        self.installer.uninstallProducts(['hph.widgets'])
        self.assertFalse(self.installer.isProductInstalled('hph.widgets'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IHphWidgetsLayer is registered."""
        from plone.browserlayer import utils

        from hph.widgets.interfaces import IHphWidgetsLayer
        self.failUnless(IHphWidgetsLayer in utils.registered_layers())
