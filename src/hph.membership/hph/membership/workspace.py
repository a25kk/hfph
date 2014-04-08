from Acquisition import aq_inner
from five import grok
from plone import api

from plone.dexterity.content import Container

from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable

from hph.membership import MessageFactory as _


class IWorkspace(form.Schema, IImageScaleTraversable):
    """
    Personal workspace container for members
    """


class Workspace(Container):
    grok.implements(IWorkspace)
    pass


class View(grok.View):
    grok.context(IWorkspace)
    grok.require('cmf.ModifyPortalContent')
    grok.name('view')

    def update(self):
        self.flash_msg = self.display_welcome_msg()

    def display_welcome_msg(self):
        return self.request.get('welcome_msg', False)

    def user_info(self):
        context = aq_inner(self.context)
        info = {}
        userid = context.getId()
        user = api.user.get(username=userid)
        info['fullname'] = user.getProperty('fullname', '') or userid
        info['email'] = user.getProperty('email', _(u"No email provided"))
        info['login_time'] = user.getProperty('login_time', '')
        info['enabled'] = user.getProperty('enabled', '')
        info['confirmed'] = user.getProperty('confirmed', '')
        return info

    def is_staff(self):
        context = aq_inner(self.context)
        admin_roles = ('Manager', 'Site Administrator', 'StaffMember')
        is_adm = False
        user = api.user.get_current()
        userid = user.getId()
        if userid is 'zope-admin':
            is_adm = True
        roles = api.user.get_roles(username=userid, obj=context)
        for role in roles:
            if role in admin_roles:
                is_adm = True
        return is_adm
