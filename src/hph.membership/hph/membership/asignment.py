# -*- coding: utf-8 -*-
"""Module providing responsible user selection and asignment"""

from five import grok
from Products.CMFCoew.interfaces import IContentish


class AsignmentView(grok.View):
    """ Group selection to provide prefiltering of users """
    grok.context(IContentish)
    grok.require('cmf.ManagePortal')
    grok.name('asignment-view')
