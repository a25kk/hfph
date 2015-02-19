# -*- coding: utf-8 -*-
"""Module providing responsible user selection and asignment"""

from five import grok
from plone import api
from Products.CMFCore.interfaces import IContentish

from hph.membership import MessageFactory as _


class AsignmentView(grok.View):
    """ Group selection to provide prefiltering of users """
    grok.context(IContentish)
    grok.require('cmf.ManagePortal')
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


class AsignmentUsers(grok.View):
    """ User selection from preselected group """
    grok.context(IContentish)
    grok.require('cmf.ManagePortal')
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
            info['email'] = user.getProperty('email', _(u"No email provided"))
            user.append(info)
        return users


class Asignment(grok.View):
    """ Process user asignment """
    grok.context(IContentish)
    grok.require('cmf.ManagePortal')
    grok.name('asignment')
