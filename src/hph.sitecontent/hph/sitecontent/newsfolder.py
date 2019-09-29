# -*- coding: utf-8 -*-
"""Module providing news folder content type"""
from plone.dexterity.content import Container
from plone.directives import dexterity, form
from zope.interface import implementer


class INewsFolder(form.Schema):
    """
    A folder acting as a collection for news items
    """


@implementer(INewsFolder)
class NewsFolder(Container):
    pass
