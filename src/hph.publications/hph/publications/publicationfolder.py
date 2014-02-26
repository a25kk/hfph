from Acquisition import aq_inner
from five import grok

from zope.lifecycleevent import modified
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
        results = catalog(object_provides=IPublication.__identifier__,
                          sort_on='getObjPositionInParent',
                          review_state='published')
        return IContentListing(results)


class CleanupView(grok.View):
    grok.context(IPublicationFolder)
    grok.require('zope2.View')
    grok.name('cleanup-publications')

    def update(self):
        self.has_publications = len(self.publications()) > 0

    def render(self):
        idx = self._cleanup_schema()
        return 'Cleaned up {0} publications'.format(idx)

    def _cleanup_schema(self):
        items = self.publications()
        idx = 0
        for item in items:
            i = item.getObject()
            media = getattr(i, 'medium')
            series = getattr(i, 'series')
            display = getattr(i, 'display')
            setattr(i, 'pubMedia', media)
            setattr(i, 'pubSeries', series)
            setattr(i, 'thirdPartyProject', display)
            idx += 1
            modified(i)
            i.reindexObject(idxs='modified')
        return idx

    def publications(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IPublication.__identifier__,
                          sort_on='getObjPositionInParent')
        return IContentListing(results)
