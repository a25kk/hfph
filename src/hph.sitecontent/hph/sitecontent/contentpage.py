from five import grok
from plone import api
from zope import schema
from plone.directives import dexterity, form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText

from hph.sitecontent import MessageFactory as _


class IContentPage(form.Schema, IImageScaleTraversable):
    """
    A content page type including fulltext and preview image
    """
    headline = schema.TextLine(
        title=_(u"Content Headline"),
        description=_(u"Optional custom headline to seperate navigation and "
                      u"content title"),
        reuired=False,
    )
    text = RichText(
        title=_(u"Text"),
        required=True
    )
    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload preview image that can be used in search "
                      u"results and listings."),
        required=False
    )


class ContentPage(dexterity.Container):
    grok.implements(IContentPage)


class View(grok.View):
    grok.context(IContentPage)
    grok.require('zope2.View')
    grok.name('view')
