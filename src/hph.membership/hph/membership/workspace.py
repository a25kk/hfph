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

    def user_info(self):
        context = aq_inner(self.context)
        info = {}
        workspace_id = context.getId()
        current_user = api.user.get_current()
        userid = current_user.getId()
        user = api.user.get(username=workspace_id)
        ownership = False
        if workspace_id == userid:
            ownership = True
            user = current_user
        info['owner'] = ownership
        info['fullname'] = user.getProperty('fullname', '') or userid
        info['email'] = user.getProperty('email', '')
        info['login_time'] = user.getProperty('login_time', '')
        info['enabled'] = user.getProperty('enabled', '')
        info['confirmed'] = user.getProperty('confirmed', '')
        return info
