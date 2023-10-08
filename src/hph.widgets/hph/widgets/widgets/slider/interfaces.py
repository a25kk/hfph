# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from zope import schema
from zope.interface import Interface, provider

from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as named_file

from ade25.panelpage import MessageFactory as _


@provider(IFormFieldProvider)
class IHPHWidgetSlider(Interface):
    """ Content Widget Slider """
    pass


@provider(IFormFieldProvider)
class IHPHWidgetSliderItem(Interface):
    """ Slide """

    text = RichText(
        title=_(u"Text"),
        required=False
    )
    image = named_file.NamedBlobImage(
        title=_(u"Slide Image"),
        required=True
    )
    image_caption = schema.TextLine(
        title=_(u"Image Copyright Information"),
        required=False
    )
