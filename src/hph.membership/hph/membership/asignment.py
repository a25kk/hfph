# -*- coding: utf-8 -*-
"""Module providing responsible user selection and asignment"""

from DateTime import DateTime
from Acquisition import aq_inner
from five import grok
from plone import api
from Products.CMFCore.interfaces import IContentish
from zope.component import getUtility

from hph.membership.tool import IHPHMemberTool
from hph.membership import MessageFactory as _


class AsignmentView(grok.View):
    """ Group selection to provide prefiltering of userers """
    grok.context(IContentish)
    grok.require('cmf.ModifyPortalContent')
    grok.name('asignment-view')

    def selectable_groups(self):
        groups = [
            'Mediengruppe',
            'Lehrende',
            'HiWi',
            'Mediengruppe',
            'Tutoren'
        ]
        return groups

    def available_groups(self):
        return api.group.get_groups()

    def groups(self):
        groups = []
        for g in self.available_groups():
            group_id = g.id
            if group_id in self.selectable_groups():
                group = {}
                group['name'] = g
                group['users'] = len(api.user.get_users(groupname=group_id))
                groups.append(group)
        return groups

    def active_asignments(self):
        context = aq_inner(self.context)
        asigned = list()
        for user_id, roles in context.get_local_roles():
            try:
                user = api.user.get(username=user_id)
                wl = user.getProperty('worklist')
                userinfo = {}
                userinfo['userid'] = user_id
                userinfo['worklist'] = wl
                userinfo['name'] = user.getProperty('fullname', user_id)
                asigned.append(userinfo)
            except AttributeError:
                pass
        return asigned


class AsignmentUsers(grok.View):
    """ User selection from preselected group """
    grok.context(IContentish)
    grok.require('cmf.ModifyPortalContent')
    grok.name('asignment-users')

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def groupname(self):
        return self.traverse_subpath[0]

    def group_users(self):
        return api.user.get_users(groupname=self.groupname())

    def selectable_users(self):
        context = aq_inner(self.context)
        users = []
        idx = 0
        for record in self.group_users():
            idx += 1
            user = api.user.get(username=record.getId())
            userid = user.getId()
            info = {}
            info['idx'] = idx
            info['userid'] = userid
            info['fullname'] = user.getProperty('fullname', '') or userid
            info['worklist'] = user.getProeprty('worklist', list())
            info['email'] = user.getProperty('email', _(u"No email provided"))
            info['roles'] = api.user.get_roles(username=userid, obj=context)
            users.append(info)
        return users

    def get_asignment(self, userid, worklist):
        context = aq_inner(self.context)
        roles = api.user.get_roles(username=userid, obj=context)
        if 'Contributor' in roles:
            context_uid = api.content.get_uuid(obj=context)
            if context_uid in worklist:
                return True
        return False


class Asignment(grok.View):
    """ Process user asignment """
    grok.context(IContentish)
    grok.require('cmf.ModifyPortalContent')
    grok.name('asignment')

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def render(self):
        context = aq_inner(self.context)
        user_roles = ['Reader', 'Editor', 'Contributor']
        userid = self.traverse_subpath[0]
        action = self.traverse_subpath[1]
        user = api.user.get(username=userid)
        worklist = user.getProperty('worklist', list())
        wl = list(worklist)
        uuid = api.content.get_uuid(obj=context)
        if action == 'revoke':
            # Disable due to issues in plone.api and unmerged pull request
            # ref: https://github.com/plone/plone.api
            # api.user.revoke_roles(
            #     username=userid,
            #     roles=user_roles,
            #     obj=context,
            # )
            context.manage_delLocalRoles([userid])
            if uuid in wl:
                wl.remove(uuid)
        else:
            api.user.grant_roles(
                username=userid,
                roles=user_roles,
                obj=context
            )
            wl.append(uuid)
        tool = getUtility(IHPHMemberTool)
        tool.update_user(userid, dict(
            login_time=DateTime(),
            worklist=tuple(wl)
        ))
        next_url = '{0}/@@asignment-view?updated=true'.format(
            context.absolute_url())
        api.portal.show_message(
            message=_(u"Responsible user asignment successfully updated"),
            request=self.request)
        return self.request.response.redirect(next_url)
