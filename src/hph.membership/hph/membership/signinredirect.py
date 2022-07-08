# -*- coding: utf-8 -*-
"""Module providing login redirects"""
from plone import api
from plone.login.interfaces import IRedirectAfterLogin
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implementer


@implementer(IUserLoggedInEvent)
class RedirectAfterLoginAdapter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, came_from=None, is_initial_login=False):
        portal = api.portal.get()
        member_folder = portal['ws']
        member_folder_url = member_folder.absolute_url()
        if 'Staff' in api.user.get_roles():
            api.portal.show_message(u'Get to work!', self.request)
            came_from = self.context.portal_url() + '/@@full_review_list'
        else:
            user = api.user.get_current()
            fullname = safe_unicode(user.getProperty('fullname'))
            api.portal.show_message(u'Nice to see you again, {0}!'.format(
                fullname),
                self.request
            )
        if not came_from:
            came_from = member_folder_url
        return came_from
