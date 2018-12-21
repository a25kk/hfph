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

CLOSE = u'<svg class="app-nav__toggle-icon" id="nav-toggle-close" xmlns="http://www.w3.org/2000/svg" version="1.1" width="100%" height="100%" viewBox="0 0 36 36"><polygon fill-rule="evenodd" points="27.8999.515 26.485 8.101 18 16.586 9.514 8.101 8.1 9.515 16.586 18 8.1 26.486 9.514 27.9 18 19.414 26.485 27.9 27.899 26.486 19.414 18"></polygon></svg>'  # noqa

OPEN = u'<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 36 36"><polygon fill-rule="evenodd" points="14.707 26.707 13.293 25.293 20.586 18 13.293 10.707 14.707 9.293 23.414 18"/></svg>'  #noqa

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

        required=False,missing_value=list(),
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

    navigation_element_close = schema.Text(
        title=_(u'Navigation Close Element'),
        description=_(u'Element used as close trigger that may contain '
                      u'svg icon code.'),
        default=CLOSE,
        missing_value=u'',
        required=True
    )

    navigation_element_open = schema.Text(
        title=_(u'Navigation Open Element'),
        description=_(u'Element used as navigation dropdown trigger.'
                      u'Warning: please make sure to keep the placeholder '
                      u'that allow to interpolate the required classes by '
                      u'the nav tree recursive renderer.'),
        default=OPEN,
        missing_value=u'',
        required=True
    )


class HphBaseControlPanelNavigationForm(RegistryEditForm):
    schema = IHphBaseControlPanelNavigation
    schema_prefix = "hph.base"
    label = u'HfPH Responsive Navigation Settings'


HphBaseSettingsNavigation = layout.wrap_form(
    HphBaseControlPanelNavigationForm,
    ControlPanelFormWrapper
)
