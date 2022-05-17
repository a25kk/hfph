# -*- coding: UTF-8 -*-

from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from five import grok
from hph.publications.publication import IPublication
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from z3c.form import form
from zope.lifecycleevent import modified
from zope.schema.vocabulary import getVocabularyRegistry

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
        self.has_publications = len(self.all_publications()) > 0
        self.filter = self.request.get('content_filter', None)

    def filtered(self):
        return self.filter is True

    def parent_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def all_publications(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IPublication.__identifier__,
                          sort_on='getObjPositionInParent',
                          review_state='published')
        return IContentListing(results)

    def publications(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        query = self._base_query()
        if self.filter is not None:
            for value in self.request.form:
                query[value] = self.request.form[value]
        results = catalog.searchResults(query)
        return IContentListing(results)

    def _base_query(self):
        context = aq_inner(self.context)
        obj_provides = IPublication.__identifier__
        query_path = '/'.join(context.getPhysicalPath())
        return dict(object_provides=obj_provides,
                    path=query_path,
                    sort_on='publicationYear',
                    sort_order='reverse',
                    review_state='published')

    def media_filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.publications.publicationMedia')
        return vocab

    def series_filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.publications.publicationSeries')
        return vocab

    def has_active_filter(self):
        req = self.request
        filtered = False
        if req.get('media') or req.get('bookSeries'):
            filtered = True
        return filtered

    def computed_klass(self, fieldname, value):
        context = aq_inner(self.context)
        active_filter = getattr(context, fieldname, None)
        klass = 'nav-item-plain'
        if active_filter == value:
            klass = 'active'
        return klass


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
