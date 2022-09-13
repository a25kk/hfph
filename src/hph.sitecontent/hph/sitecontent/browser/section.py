# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
from plone import api
from plone.app.z3cform.utils import replace_link_variables_by_paths

from Acquisition import aq_inner
from Products.Five.browser import BrowserView


class MainSectionView(BrowserView):
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

    def has_panel_layout(self):
        context = aq_inner(self.context)
        try:
            panel_layout = context.panelPageLayout
        except AttributeError:
            panel_layout = None
        if panel_layout is not None:
            return True
        return False

    def content_widget(self, widget='base'):
        """ Backwards compatible widget integration that allows for
            direct template level integration of widgets
         """
        context = aq_inner(self.context)
        requested_widget = widget
        widget_view_name = '@@content-widget-{0}'.format(
            requested_widget
        )
        template = context.restrictedTraverse(widget_view_name)(
            widget_type=requested_widget,
            identifier=requested_widget
        )
        return template
