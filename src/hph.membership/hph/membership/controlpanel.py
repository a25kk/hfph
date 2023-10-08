# from five import grok
from Products.CMFCore.interfaces import ISiteRoot

from plone.z3cform import layout
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from hph.membership.interfaces import IHPHMembershipTool
from hph.membership.interfaces import IHPHMembershipSettings


class HPHMembershipSettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IHPHMembershipSettings
    label = u"HPH membership tool settings"


class HPHMembershipSettingsView(grok.View):
    """
        View which wrap the settings form using ControlPanelFormWrapper
        to a HTML boilerplate frame.
    """
    grok.name("hph-membershiptool-settings")
    grok.layer(IHPHMembershipTool)
    grok.context(ISiteRoot)

    def render(self):
        view_factor = layout.wrap_form(HPHMembershipSettingsEditForm,
                                       ControlPanelFormWrapper)
        view = view_factor(self.context, self.request)
        return view()
