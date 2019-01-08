# -*- coding: utf-8 -*-
"""Module providing faculty member views"""
from Acquisition import aq_inner
from Products.Five import BrowserView
from hph.faculty.facultymember import IFacultyMember
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from zope.schema.vocabulary import getVocabularyRegistry


class FacultyListing(BrowserView):

    def __call__(self, **kw):
        self.filter = self.request.get('content_filter', None)
        return self.render()

    def render(self):
        return self.index()

    def filtered(self):
        return self.filter is True

    def content_filter(self):
        context = aq_inner(self.context)
        tmpl = context.restrictedTraverse('@@content-filter-faculty')()
        return tmpl

    def faculty_members(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        query = self._base_query()
        if self.filter is not None:
            query['academicRole'] = self.request.get('academicRole', '')
        results = catalog.searchResults(query)
        return IContentListing(results)

    def _base_query(self):
        context = aq_inner(self.context)
        obj_provides = IFacultyMember.__identifier__
        query_path = '/'.join(context.getPhysicalPath())
        return dict(
            object_provides=obj_provides,
            path=query_path,
            review_state='published',
            sort_on='lastname',
            academicRole='professor'
        )


class FacultyListingFilter(BrowserView):

    def __call__(self, **kw):
        self.filter = self.request.get('academicRole', None)
        return self.render()

    def render(self):
        return self.index()

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def computed_klass(self, value):
        css_class = 'c-nav-list__item'
        if value == 'professor' and not self.filter:
            css_class = 'c-nav-list__item--active'
        if self.filter == value:
            css_class = 'c-nav-list__item--active'
        return css_class
