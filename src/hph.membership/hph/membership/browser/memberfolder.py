# -*- coding: utf-8 -*-
"""Module providing definitions"""
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView


class MemberFolderView(BrowserView):
    """ Blog view """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, **kw):
        self.available = self.has_view_permission()
        self.is_anon = api.user.is_anonymous()
        return self.render()

    def render(self):
        return self.request.response.redirect(self.workspace_url())

    def workspace_url(self):
        context = aq_inner(self.context)
        here_url = context.absolute_url()
        user = api.user.get_current()
        userid = user.getId()
        if userid in list(context.keys()):
            url = '{0}/{1}'.format(here_url, userid)
        else:
            url = '{0}/@@workspace-missing'.format(here_url)
        return url

    def usermanager_url(self):
        context = aq_inner(self.context)
        here_url = context.absolute_url()
        url = '{0}/@@user-manager'.format(here_url)
        return url

    def has_view_permission(self):
        context = aq_inner(self.context)
        admin_roles = ('Manager', 'Site Administrator', 'StaffMember')
        is_adm = False
        if not api.user.is_anonymous():
            user = api.user.get_current()
            userid = user.getId()
            if userid is 'zope-admin':
                is_adm = True
            roles = api.user.get_roles(username=userid, obj=context)
            for role in roles:
                if role in admin_roles:
                    is_adm = True
        return is_adm


class WorkspaceMissingView(BrowserView):
    """ Browser View """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, **kw):
        return self.render()

    def render(self):
        return self.index()
