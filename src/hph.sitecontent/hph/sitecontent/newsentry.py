from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone.directives import dexterity, form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText

from hph.sitecontent import MessageFactory as _


class INewsEntry(form.Schema, IImageScaleTraversable):
    """
    A news or announcement item
    """
    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload a preview image that will be used in news "
                      u"teasers."),
        required=True,
    )
    text = RichText(
        title=_(u"Main Text"),
        required=True,
    )


class NewsEntry(dexterity.Container):
    grok.implements(INewsEntry)


class View(grok.View):
    grok.context(INewsEntry)
    grok.require('zope2.View')
    grok.name('view')

    def parent_url(self):
        parent = aq_parent(aq_inner(self.context))
        return parent.absolute_url()
