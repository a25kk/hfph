from zope.interface import implementer
from zope.schema.vocabulary import getVocabularyRegistry

# # from five import grok
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.dexterity.content import Container
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model

from Acquisition import aq_inner
from z3c.form import form

from hph.faculty import MessageFactory as _
from hph.faculty.facultymember import IFacultyMember


class IFacultyDirectory(model.Schema, IImageScaleTraversable):
    """
    A directory of faculty staff members
    """


@implementer(IFacultyDirectory)
class FacultyDirectory(Container):
    pass


class View(object):

    def update(self):
        self.filter = self.request.get('content_filter', None)

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
        return dict(object_provides=obj_provides,
                    path=query_path,
                    review_state='published',
                    sort_on='lastname',
                    academicRole='professor'
                    )


class ContentFilter(object):

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def computed_klass(self, value):
        active_filter = self.request.get('academicRole', None)
        klass = 'app-nav-list-item'
        if value == 'professor' and not active_filter:
            klass = 'app-nav-list-item-active'
        if active_filter == value:
            klass = 'app-nav-list-item-active'
        return klass
