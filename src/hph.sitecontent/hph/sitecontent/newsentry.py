from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone import api
from plone.directives import dexterity, form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText
from plone.supermodel import model

from hph.sitecontent import MessageFactory as _
from plone.supermodel.directives import fieldset
from zope import schema


class INewsEntry(model.Schema, IImageScaleTraversable):
    """
    A news or announcement item
    """
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
    text = RichText(
        title=_(u"Main Text"),
        required=True,
    )


class NewsEntry(dexterity.Container):
    grok.implements(INewsEntry)
