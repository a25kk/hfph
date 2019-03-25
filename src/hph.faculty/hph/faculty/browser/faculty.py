# -*- coding: utf-8 -*-
"""Module providing faculty member views"""
from Acquisition import aq_inner, aq_parent
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
        context = aq_inner(self.context)
        css_class = 'c-nav-list__item'
        if IFacultyMember.providedBy(context):
            academic_role = getattr(context, 'academicRole', None)
            if academic_role and academic_role == value:
                css_class = 'c-nav-list__item--active'
        else:
            if value == 'professor' and not self.filter:
                css_class = 'c-nav-list__item--active'
            if self.filter == value:
                css_class = 'c-nav-list__item--active'
        return css_class


class FacultyMember(BrowserView):

    def parent_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def item_owner(self):
        if api.user.is_anonymous():
            return False
        context = aq_inner(self.context)
        is_owner = False
        user = api.user.get_current()
        if user.getId() in context.listCreators():
            is_owner = True
        return is_owner

    def content_filter(self):
        context = aq_inner(self.context)
        container = aq_parent(context)
        tmpl = container.restrictedTraverse('@@content-filter-faculty')()
        return tmpl

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def computed_klass(self, value):
        context = aq_inner(self.context)
        active_filter = getattr(context, 'academicRole', None)
        klass = 'nav-item-plain'
        if active_filter == value:
            klass = 'active'
        return klass

    def show_address(self):
        context = aq_inner(self.context)
        display = False
        if context.street or context.email:
            display = True
        return display

    def has_publications(self):
        context = aq_inner(self.context)
        try:
            content = context.associatedPublications
        except AttributeError:
            content = None
        if content is not None:
            return True
        return False
