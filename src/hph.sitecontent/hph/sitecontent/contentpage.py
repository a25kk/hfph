# -*- coding: utf-8 -*-
"""Module providing content page type"""
from five import grok
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import implementer

from hph.sitecontent import MessageFactory as _


class IContentPage(model.Schema, IImageScaleTraversable):
    """
    A content page type including fulltext and preview image
    """
    headline = schema.TextLine(
        title=_(u"Content Headline"),
        description=_(u"Optional custom headline to seperate navigation and "
                      u"content title"),
        required=False,
    )
    text = RichText(
        title=_(u"Text"),
        required=False
    )

    fieldset(
        'media',
        label=_(u"Media"),
        fields=['image', 'image_caption']
    )

    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload preview image that can be used in search "
                      u"results and listings."),
        required=False
    )

    image_caption = schema.TextLine(
        title=_(u"Cover Image Caption"),
        required=False
    )


@implementer(IContentPage)
class ContentPage(Container):
    pass
