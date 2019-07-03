# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as named_file
from zope import schema
from zope.interface import Interface, provider

from ade25.panelpage import MessageFactory as _


@provider(IFormFieldProvider)
class IHPHWidgetAccordion(Interface):
    """ Content Widget Accordion """
    pass


@provider(IFormFieldProvider)
class IHPHWidgetAccordionItem(Interface):
    """ Slide """

    title = schema.TextLine(
        title=_(u"Panel Headline"),
        required=False
    )

    text = RichText(
        title=_(u"Panel Content"),
        required=False
    )
