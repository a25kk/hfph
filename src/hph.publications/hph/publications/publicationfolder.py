from Acquisition import aq_inner
from five import grok
from plone.directives import dexterity, form

from Products.CMFCore.utils import getToolByName

from plone.app.contentlisting.interfaces import IContentListing

from hph.publications.publication import IPublication

from hph.publications import MessageFactory as _


class IPublicationFolder(form.Schema):
    """
    A  central collection of publications with filter functionality
    """


class PublicationFolder(dexterity.Container):
    grok.implements(IPublicationFolder)


class View(grok.View):
    grok.context(IPublicationFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_publications = len(self.publications()) > 0

    def publications(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IPublication.__identifier__,)
        return IContentListing(results)
