# -*- coding: utf-8 -*-
"""Module providing control panel views"""
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface

from hph.sitecontent import MessageFactory as _


class HphBaseSettings(BrowserView):
    """ Ade25 settings overview """

    def update(self):
        if super(HphBaseSettings, self).update():
            if 'form.button.setup' in self.request.form:
                self.process_setup()

    def process_setup(self):
        IStatusMessage(self.request).addStatusMessage(
            _(u'Setup initialized.'), 'info')


class IHphBaseControlPanelNavigation(Interface):
    """ Navigation settings """

    display_home_link = schema.Bool(
        title=_(u"Enable Home Link"),
        description=_(u"Choose if the main navigation should include a home "
                      u"link pointing at the front page."),
        default=False,
        required=False
    )

    listed_content_types = schema.List(
        title=_(u"Listed Content Types"),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'
        ),
        default=list(),
        missing_value=list(),
        required=False,
    )

    navigation_root = schema.TextLine(
        title=_(u'Root'),
        description=_(
            u'Path to be used as navigation root, relative to Plone site root.'
            u'Starts with \'/\''
        ),
        default=u'/',
        required=True
    )

    navigation_depth = schema.Int(
        title=_(u'Navigation depth'),
        description=_(u'Number of folder levels to show in the '
                      u'site navigation.'),
        default=3,
        required=True
    )


class HphBaseControlPanelNavigationForm(RegistryEditForm):
    schema = IHphBaseControlPanelNavigation
    schema_prefix = "hph.sitecontent"
    label = u'HfPH Responsive Navigation Settings'


HphBaseSettingsNavigation = layout.wrap_form(
    HphBaseControlPanelNavigationForm,
    ControlPanelFormWrapper
)
