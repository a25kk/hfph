# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from zope import schema
from zope.interface import Interface, provider

from plone.autoform.interfaces import IFormFieldProvider

from ade25.panelpage import MessageFactory as _


@provider(IFormFieldProvider)
class IHPHWidgetContentAlias(Interface):
    """ Content Widget to display external content via references """

    alias = schema.TextLine(
        title=u"Content Source",
        description=_(u"Please enter the unique identifier of the target "
                      u"content item available via attaching @@uuid to the "
                      u"target object's url"),
        required=True,
    )
