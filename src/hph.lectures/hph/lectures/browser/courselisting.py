# -*- coding: utf-8 -*-
"""Module providing course listings"""
import collections

from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from hph.lectures.lecture import ILecture
from plone import api
from plone.app.contentlisting.interfaces import IContentListing

from zope.component import getMultiAdapter
from zope.schema.vocabulary import getVocabularyRegistry

from hph.lectures import vocabulary
from hph.lectures import MessageFactory as _


class CourseListing(BrowserView):
    """ Edit course module data via basic form """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.errors = {}
        self.filter = self.request.get('content_filter', None)
        self.has_archives = len(self.contained_course_folders()) > 0
        return self.render()

    def update(self):
        translation_service = api.portal.get_tool(name="translation_service")
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('selector_degree_courses', )
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            errorIdx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {}
                        error_msg = _(u"This field is required")
                        error['active'] = True
                        error['msg'] = translation_service.translate(
                            error_msg,
                            'hph.lectures',
                            target_language=api.portal.get_default_language()
                        )
                        form_errors[value] = error
                        errorIdx += 1
                    else:
                        error = {}
                        error['active'] = False
                        error['msg'] = form[value]
                        form_errors[value] = error
            if errorIdx > 0:
                self.errors = form_errors
            else:
                self.filter_courses(form_data)

    def render(self):
        self.update()
        return self.index()

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

    def contained_course_folders(self):
        context = aq_inner(self.context)
        folders = context.restrictedTraverse('@@folderListing')(
            portal_type='hph.lectures.coursefolder',
            review_state='published')
        return folders

    def is_current_view_context(self, container):
        context = aq_inner(self.context)
        active = False
        if container.getId() == context.getId():
            active = True
        return active

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.lectures.CourseType')
        return vocab

    def computed_class(self, value):
        active_filter = self.request.get('courseType', None)
        item_class = 'app-nav-list-item app-nav-list-item-plain'
        if active_filter == value:
            item_class = 'app-nav-list-item app-nav-list-item-active'
        return item_class

    @staticmethod
    def degree_courses():
        courses = vocabulary.degree_courses()
        return courses

    @staticmethod
    def get_degree_course_title(course):
        course_names = vocabulary.degree_courses_tokens()
        return course_names[course]

    @staticmethod
    def learning_modules_master():
        learning_modules = vocabulary.learning_modules_master()
        sorted_items = collections.OrderedDict(sorted(learning_modules.items()))
        return sorted_items

    @staticmethod
    def learning_modules_bachelor():
        learning_modules = vocabulary.learning_modules_bachelor()
        sorted_items = collections.OrderedDict(sorted(learning_modules.items()))
        return sorted_items

    @staticmethod
    def course_core_themes():
        return vocabulary.course_core_themes()

    def lectures(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        query = self._base_query()
        project_filter = self.request.get('project', None)
        course_filter = self.request.get('courseType', None)
        if self.filter is not None:
            if course_filter is not None:
                query['courseType'] = course_filter
            if project_filter is not None:
                query['externalFundsProject'] = project_filter
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

    @staticmethod
    def rendered_course_card(uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse('@@course-card')()
        return template

    def filter_courses(self, data):
        return


class CourseFilter(BrowserView):
    """ Edit course module data via basic form """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @staticmethod
    def degree_courses():
        courses = vocabulary.degree_courses()
        return courses

    @staticmethod
    def get_degree_course_title(course):
        course_names = vocabulary.degree_courses_tokens()
        return course_names[course]

    @staticmethod
    def learning_modules_master():
        learning_modules = vocabulary.learning_modules_master()
        sorted_items = collections.OrderedDict(sorted(learning_modules.items()))
        return sorted_items

    @staticmethod
    def learning_modules_bachelor():
        learning_modules = vocabulary.learning_modules_bachelor()
        sorted_items = collections.OrderedDict(sorted(learning_modules.items()))
        return sorted_items

    @staticmethod
    def course_core_themes():
        return vocabulary.course_core_themes()


class CourseFilterView(BrowserView):
    """ Course filter standalone view """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @staticmethod
    def rendered_course_filter_bar(context):
        context = aq_inner(context)
        template = context.restrictedTraverse('@@course-filter-bar')()
        return template


class CourseFilterSelectBox(BrowserView):
    """ Edit course module data via basic form """

    def __call__(self,
                 selector='master',
                 identifier=None,
                 target=None,
                 data_set=None,
                 visibility='visible',
                 **kw):
        field_data = self.field_data_map()
        filter_data = {
            'name': identifier,
            'selector': selector,
            'visibility': visibility,
            'target': 'undefined'
        }
        if target:
            filter_data['target'] = target
        if data_set:
            filter_data['options'] = field_data[data_set]
        filter_data.update(kw)
        self.field_options = filter_data
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def degree_courses():
        courses = vocabulary.degree_courses()
        return courses

    @staticmethod
    def get_degree_course_title(course):
        course_names = vocabulary.degree_courses_tokens()
        return course_names[course]

    @staticmethod
    def learning_modules_master():
        learning_modules = vocabulary.learning_modules_master()
        sorted_items = collections.OrderedDict(sorted(learning_modules.items()))
        return sorted_items

    @staticmethod
    def learning_modules_bachelor():
        learning_modules = vocabulary.learning_modules_bachelor()
        sorted_items = collections.OrderedDict(sorted(learning_modules.items()))
        return sorted_items

    @staticmethod
    def course_core_themes():
        return vocabulary.course_core_themes()

    def field_data_map(self):
        field_map = {
            'courses': self.degree_courses(),
            'modules-ba': self.learning_modules_bachelor(),
            'modules-ma': self.learning_modules_master(),
            'core-themes': self.course_core_themes()
        }
        for theme_key, theme_value in self.course_core_themes().items():
            map_key = 'core-theme-{0}'.format(theme_key)
            field_map[map_key] = theme_value
        return field_map
