# -*- coding: utf-8 -*-
"""Module providing views for course module editing"""
from Products.Five.browser import BrowserView
from plone import api


class CourseModuleEditor(BrowserView):
    """ Edit course module data via basic form """

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()
