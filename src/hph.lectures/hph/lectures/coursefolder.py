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
        self.has_archives = len(self.subfolders()) > 0

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

    def prettify_degree(self, value):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.lectures.CourseDegree')
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
        klass = 'app-nav-list-item app-nav-list-item-plain'
        if active_filter == value:
            klass = 'app-nav-list-item app-nav-list-item-active'
        return klass

    def contained_items(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        query = self._base_query()
        project_filter = self.request.get('project', None)
        course_filter = self.request.get('courseType', None)
        if self.filter is not None:
            if course_filter is not None:
                query['courseType'] = course_filter
            if project_filter is not None:
                query['thirdPartyProject'] = project_filter
        results = catalog.searchResults(query)
        return IContentListing(results)

    def _base_query(self):
        context = aq_inner(self.context)
        obj_provides = ILecture.__identifier__
        return dict(object_provides=obj_provides,
                    path=dict(query='/'.join(context.getPhysicalPath()),
                              depth=1),
                    review_state='published',
                    sort_on='courseNumber')

    def subfolders(self):
        context = aq_inner(self.context)
        folders = context.restrictedTraverse('@@folderListing')(
            portal_type='hph.lectures.coursefolder',
            review_state='published')
        return folders

    def is_active_folder(self, folder):
        context = aq_inner(self.context)
        active = False
        if folder.getId() == context.getId():
            active = True
        return active

    def can_edit(self):
        if api.user.is_anonymous():
            return False
        allowed = False
        context = aq_inner(self.context)
        user = api.user.get_current()
        user_id = user.getId()
        if user_id == 'zope-admin':
            allowed = True
        else:
            admin_roles = ('Manager', 'Site Administrator', 'StaffMember')
            roles = api.user.get_roles(username=user_id, obj=context)
            for role in roles:
                if role in admin_roles:
                    allowed = True
        return allowed


class XHRIntegration(grok.View):
    grok.context(ICourseFolder)
    grok.require('zope2.View')
    grok.name('xhr-integration')

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.sitecontent.thirdPartyProjects')
        return vocab
