# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from hph.sitetheme.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of hph.sitetheme into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if hph.sitetheme is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('hph.sitetheme'))

    def test_uninstall(self):
        """Test if hph.sitetheme is cleanly uninstalled."""
        self.installer.uninstallProducts(['hph.sitetheme'])
        self.assertFalse(self.installer.isProductInstalled('hph.sitetheme'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IHphSitethemeLayer is registered."""
        from hph.sitetheme.interfaces import IHphSitethemeLayer
        from plone.browserlayer import utils
        self.failUnless(IHphSitethemeLayer in utils.registered_layers())
