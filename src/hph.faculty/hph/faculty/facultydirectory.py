from Acquisition import aq_inner
from five import grok
from plone import api

from zope.schema.vocabulary import getVocabularyRegistry

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.contentlisting.interfaces import IContentListing

from hph.faculty.facultymember import IFacultyMember

from hph.faculty import MessageFactory as _


class IFacultyDirectory(form.Schema, IImageScaleTraversable):
    """
    A directory of faculty staff members
    """


class FacultyDirectory(Container):
    grok.implements(IFacultyDirectory)


class View(grok.View):
    grok.context(IFacultyDirectory)
    grok.require('zope2.View')
    grok.name('view')

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
                    review_state='published')


class ContentFilter(grok.View):
    grok.context(IFacultyDirectory)
    grok.require('zope2.View')
    grok.name('content-filter-faculty')

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def computed_klass(self, value):
        active_filter = self.request.get('academicRole', None)
        klass = 'nav-item-plain'
        if active_filter == value:
            klass = 'active'
        return klass
