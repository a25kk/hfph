# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone.app.z3cform.widget import LinkFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as named_file
from zope import schema
from zope.interface import Interface, provider

from ade25.panelpage import MessageFactory as _


@provider(IFormFieldProvider)
class IHPHWidgetImagePoster(Interface):
    """ Content Panel Storage Slots """

    title = schema.TextLine(
        title=_("Poster Headline"),
        required=False
    )
    description = schema.Text(
        title=_("Poster Text"),
        required=False
    )
    image = named_file.NamedBlobImage(
        title=_(u"Poster Image"),
        required=True
    )
    image_caption = schema.TextLine(
        title=_(u"Poster Image Copyright Information"),
        required=False
    )
    directives.widget(link=LinkFieldWidget)
    link = schema.TextLine(
        title=_(u"Link"),
        description=_(u"Please select link target"),
        required=False,
    )
