# -*- coding: utf-8 -*-
"""Module providing embeddable social sharing bar"""
from Products.Five import BrowserView


class SocialSharing(BrowserView):
    """ Embeddable card view for news entries"""

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()
