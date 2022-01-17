# -*- coding: utf-8 -*-
"""Module providing faculty member views"""
import logging

from Acquisition import aq_inner, aq_parent
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from Products.Five import BrowserView
from zope.schema.vocabulary import getVocabularyRegistry

from hph.faculty.facultymember import IFacultyMember

logger = logging.getLogger("HfPH Faculty")


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

    def filter_options_list(self):
        filter = ['professor', 'emeriti', 'lecturer']
        return filter

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def get_filter_title(self, filter):
        filter_title = self.filter_options().get(filter, '')
        return filter_title

    def active_filter(self):
        context = aq_inner(self.context)
        if IFacultyMember.providedBy(context):
            academic_role = getattr(context, 'academicRole', None)
            if academic_role:
                return academic_role
        else:
            if self.filter:
                return self.filter
            else:
                return 'professor'

    def filter_base_url(self):
        context = aq_inner(self.context)
        if IFacultyMember.providedBy(context):
            parent = aq_parent(context)
            return parent.absolute_url()
        return context.absolute_url()

    def computed_klass(self, value):
        context = aq_inner(self.context)
        css_class = 'c-nav-list__item'
        if IFacultyMember.providedBy(context):
            academic_role = getattr(context, 'academicRole', None)
            if academic_role and academic_role == value:
                css_class += ' c-nav-list__item--active'
        else:
            if value == 'professor' and not self.filter:
                css_class += ' c-nav-list__item--active'
            if self.filter == value:
                css_class += ' c-nav-list__item--active'
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

    def has_cover_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def has_publications(self):
        context = aq_inner(self.context)
        try:
            content = context.associatedPublications
        except AttributeError:
            content = None
        if content is not None:
            return True
        return False


class FacultyMemberContentFactory(BrowserView):

    def __call__(self):
        return self.render()

    def render(self):
        context = aq_inner(self.context)
        self._create_faculty_member_content()
        api.portal.show_message(
            message='Faculty member default content successfully created.',
            request=self.request
        )
        return self.request.response.redirect(context.absolute_url())

    @staticmethod
    def _create_faculty_member_content():
        content_views = {
            'publications': "Publikationen",
            'associated-lectures': "Lehrveranstaltungen"
        }
        items = api.content.find(
            context=api.portal.get(),
            portal_type="hph.faculty.facultymember"
        )
        for item in items:
            if 'publikationen' not in item.keys():
                # handle content creation
                faculty_member = item.getObject()
                url_path = faculty_member.absolute_url_path()
                for view_name, title in content_views.items():
                    content_object = api.content.create(
                        container=faculty_member,
                        type='Link',
                        title=title,
                        remoteUrl='{url}/@@{view}'.format(
                            url=url_path,
                            view=view_name
                        )
                    )
                    api.content.transition(
                        content_object,
                        transition='publish'
                    )
                    logger.info(" - created content for {0}".format(url_path))
