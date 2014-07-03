from Acquisition import aq_inner
from five import grok
from plone import api

from plone.dexterity.content import Container

from plone.directives import form
from plone.keyring import django_random
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
        info['login_time'] = user.getProperty('last_login_time', '')
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

    def group_actions(self):
        context = aq_inner(self.context)
        userid = context.getId()
        groups = api.group.get_groups(username=userid)
        actions = []
        return actions

    def compose_pwreset_link(self):
        context = aq_inner(self.context)
        user_id = context.getId()
        user = api.user.get(username=user_id)
        token = self._access_token(user)
        portal_url = api.portal.get().absolute_url()
        url = '{0}/useraccount/{1}/{2}'.format(
            portal_url, user_id, token)
        return url

    def _access_token(self, user):
        stored_token = user.getProperty('token', '')
        if len(stored_token):
            token = stored_token
        else:
            token = django_random.get_random_string(length=12)
            user.setMemberProperties(mapping={'token': token})
        return token
