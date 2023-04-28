# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
from plone import api
from plone.app.z3cform.utils import replace_link_variables_by_paths

from Acquisition import aq_inner
from Products.Five.browser import BrowserView


class LanguageRootView(BrowserView):
    """ Site section default view """

    def __call__(self):
        if api.user.is_anonymous() and self.has_link_action():
            link_target = self.get_link_action()
            self.request.response.redirect(link_target)
        else:
            return self.render()

    def render(self):
        return self.index()

    def has_link_action(self):
        context = aq_inner(self.context)
        try:
            context_link = context.link
        except AttributeError:
            context_link = None
        if context_link is not None:
            return True
        return False

    def get_link_action(self):
        context = aq_inner(self.context)
        link = context.link
        link_action = replace_link_variables_by_paths(context, link)
        return link_action

    @staticmethod
    def is_authenticated():
        return not api.user.is_anonymous()
