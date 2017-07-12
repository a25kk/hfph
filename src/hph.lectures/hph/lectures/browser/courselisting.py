# -*- coding: utf-8 -*-
"""Module providing course listings"""
from Products.Five import BrowserView


class CourseListing(BrowserView):
    """ Edit course module data via basic form """

    def __call__(self):
        self.errors = {}
        return self.render()