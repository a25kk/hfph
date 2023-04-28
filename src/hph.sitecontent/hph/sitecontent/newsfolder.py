# -*- coding: utf-8 -*-
"""Module providing news folder content type"""
from zope.interface import implementer

from plone.dexterity.content import Container
from plone.supermodel import model

from z3c.form import form


class INewsFolder(model.Schema):
    """
    A folder acting as a collection for news items
    """


@implementer(INewsFolder)
class NewsFolder(Container):
    pass
