# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as named_file
from zope import schema
from zope.interface import Interface, provider

from ade25.panelpage import MessageFactory as _


@provider(IFormFieldProvider)
class IHPHWidgetImagePoster(Interface):
    """ Content Panel Storage Slots """

    image = named_file.NamedBlobImage(
        title=_(u"Poster Image"),
        required=True
    )
    image_caption = schema.TextLine(
        title=_(u"Poster Image Copyright Information"),
        required=False
    )
    text = RichText(
        title=_(u"Text"),
        required=False,
        allowed_mime_types=('text/html', ),
    )
