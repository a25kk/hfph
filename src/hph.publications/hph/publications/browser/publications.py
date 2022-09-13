# -*- coding: utf-8 -*-
"""Module providing publication browser views"""
from zope.schema.vocabulary import getVocabularyRegistry

from plone import api
from plone.app.contentlisting.interfaces import IContentListing

from Acquisition import aq_inner, aq_parent
from Products.Five import BrowserView

from hph.publications.publication import IPublication


class PublicationsListView(BrowserView):
    """ List of publications"""

    def __call__(self):
        self.has_publications = len(self.publications()) > 0
        self.filter = self.request.get('content_filter', None)
        return self.render()

    def render(self):
        return self.index()

    def filter(self):
        return self.request.get('content_filter', None)

    def filtered(self):
        return self.filter is True

    def parent_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def all_publications(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool('portal_catalog')
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
        return results

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

    def computed_klass(self, filter_name, value):
        klass = 'c-nav-list__link'
        if self.filter:
            active_filter = getattr(self.request, filter_name, None)
            if active_filter == value:
                klass += ' c-nav-list__link--active'
        return klass
