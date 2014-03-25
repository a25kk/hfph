from Acquisition import aq_inner
from five import grok
from plone import api

from zope.schema.vocabulary import getVocabularyRegistry

from plone.dexterity.content import Container

from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.contentlisting.interfaces import IContentListing

from hph.lectures.lecture import ILecture

from hph.lectures import MessageFactory as _


class ICourseFolder(form.Schema, IImageScaleTraversable):
    """
    Manage lectures
    """


class CourseFolder(Container):
    grok.implements(ICourseFolder)
    pass


class View(grok.View):
    grok.context(ICourseFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.filter = self.request.get('content_filter', None)

    def prettify_duration(self, value):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.lectures.CourseDuration')
        title = _(u"undefined")
        if value is not None:
            for term in vocab:
                if term.value == value:
                    title = term.title
        return title

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.lectures.CourseType')
        return vocab

    def computed_klass(self, value):
        active_filter = self.request.get('courseType', None)
        klass = 'nav-item-plain'
        if active_filter == value:
            klass = 'active'
        return klass

    def contained_items(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        query = self._base_query()
        if self.filter is not None:
            query['courseType'] = self.request.get('courseType', '')
        results = catalog.searchResults(query)
        return IContentListing(results)

    def _base_query(self):
        context = aq_inner(self.context)
        obj_provides = ILecture.__identifier__
        query_path = '/'.join(context.getPhysicalPath())
        return dict(object_provides=obj_provides,
                    path=query_path,
                    review_state='published',
                    sort_on='courseNumber')
