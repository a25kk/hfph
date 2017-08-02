# -*- coding: utf-8 -*-
"""Module providing course listings"""
import collections
import hashlib
import json
import uuid

from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from hph.lectures.interfaces import ICourseFilterTool
from hph.lectures.lecture import ILecture
from plone import api
from plone.keyring import django_random

from zope.component import getMultiAdapter, getUtility
from zope.schema.vocabulary import getVocabularyRegistry

from hph.lectures import vocabulary
from hph.lectures import MessageFactory as _


class CourseListing(BrowserView):
    """ Edit course module data via basic form """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, **kw):
        self.errors = {}
        self.filter = self.request.get('content_filter', None)
        self.has_archives = len(self.contained_course_folders()) > 0
        self.query = self._base_query()
        self.query.update(kw)
        self.results = self.lectures()
        self.result_count = len(self.results)
        if self.is_current_semester():
            return self.render()
        else:
            if self.has_archives:
                current_semester_folder = self.get_highlighted_container()
                next_url = current_semester_folder.getURL()
                return self.request.response.redirect(next_url)
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
                self._update_query(form_data)

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

    def is_current_semester(self):
        context = aq_inner(self.context)
        current_marker = getattr(context, 'is_current_semester', None)
        return current_marker

    def _update_query(self, form_data):
        context = aq_inner(self.context)
        name = 'course-filter'
        filter_data = form_data
        tool = getUtility(ICourseFilterTool)
        if not self.has_active_session():
            session_token = self.generate_session_token()
            filter_data['token'] = session_token
            stored_data = tool.create_record(session_token, filter_data)
        else:
            session_data = tool.get()
            stored_data = session_data[name]
        updated_filters = stored_data['filter']
        for key, value in form_data.items():
            if key == 'degree-course':
                # Clean possible duplicates
                if not isinstance(value, basestring):
                    updated_filters[key] = list(set(value))
            else:
                updated_filters[key] = value
        if updated_filters:
            stored_data['filter'] = updated_filters
            tool.add(name, stored_data)
        return self.request.response.redirect(context.absolute_url())

    def contained_course_folders(self):
        context = aq_inner(self.context)
        folders = context.restrictedTraverse('@@folderListing')(
            portal_type='hph.lectures.coursefolder',
            review_state='published')
        return folders

    def get_highlighted_container(self):
        sub_folders = self.contained_course_folders()
        for folder in sub_folders:
            container = folder.getObject()
            current_marker = getattr(container, 'is_current_semester', None)
            if current_marker:
                return folder
        return sub_folders[0]

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
        query = self.query
        project_filter = self.request.get('project', None)
        course_filter = self.request.get('courseType', None)
        # URL parameter bases content filters have presence of stored
        # or preselected values inside the session
        if self.filter is not None:
            if course_filter is not None:
                query['courseType'] = course_filter
            if project_filter is not None:
                query['externalFundsProject'] = project_filter
        else:
            # Use stored filter session
            if self.has_active_session():
                blacklist = ('token', )
                stored_data = self.stored_filters()['course-filter']
                if 'filter' in stored_data:
                    filter_list = list()
                    for key, value in stored_data['filter'].items():
                        if key not in blacklist:
                            if key == 'course-types':
                                query['courseType'] = value
                            else:
                                filter_list.append(value)
                    if filter_list:
                        query['courseModules'] = filter_list
        results = catalog.searchResults(query)
        # import pdb; pdb.set_trace()
        return results

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
        template = context.restrictedTraverse('@@course-card')(
            preview=True
        )
        return template

    @staticmethod
    def rendered_course_filter_bar(context):
        context = aq_inner(context)
        template = context.restrictedTraverse('@@course-filter-bar')()
        return template

    @staticmethod
    def generate_session_token():
        random_salt = django_random.get_random_string()
        return hashlib.sha1(str(uuid.uuid4()) + random_salt).hexdigest()

    def has_active_session(self):
        active = False
        try:
            session = self.stored_filters()
        except KeyError:
            session = None
        if session:
            active = True
        return active

    @staticmethod
    def stored_filters():
        tool = getUtility(ICourseFilterTool)
        return tool.get()

    def active_filters(self):
        stored_data = self.stored_filters()
        if 'course-filter' in stored_data:
            filter_data = stored_data['course-filter']
            if 'filter' in filter_data:
                active_filters = dict()
                filters = filter_data['filter']
                for key, value in filters.items():
                    if key != 'token':
                        active_filters[key] = value
                return active_filters
            else:
                return None

    def active_type_filter(self):
        active_filters = self.active_filters()
        if active_filters and 'course-types' in active_filters:
            filter_options = self.filter_options()
            course_type = active_filters['course-types']
            filter_term = filter_options.getTermByToken(course_type)
            return filter_term.title
        return None

    def active_course_filter(self):
        active_filters = self.active_filters()
        if active_filters and 'degree-course' in active_filters:
            filter_token = active_filters['degree-course']
            filter_term = self.get_degree_course_title(filter_token)
            return filter_term
        return None

    def active_course_module_filter(self):
        active_filters = self.active_filters()
        if active_filters and 'course-modules--master' in active_filters:
            filter_token = active_filters['course-modules--master']
            return filter_token
        if active_filters and 'course-modules--bachelor' in active_filters:
            filter_token = active_filters['course-modules--bachelor']
            filter_term = self.learning_modules_bachelor()[filter_token]
            return filter_term
        return None

    def active_course_theme_filter(self):
        active_filters = self.active_filters()
        if active_filters:
            for filter_item in active_filters:
                if filter_item.startswith('core-theme'):
                    filter_token = active_filters[filter_item]
                    theme_id = filter_item.split('--')[1]
                    theme_list = self.course_core_themes()[theme_id]
                    return theme_list[filter_token]
        return None


class CourseFilter(BrowserView):
    """ Edit course module data via basic form """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def has_active_session(self):
        active = False
        try:
            session = self.stored_filters()
        except KeyError:
            session = None
        if session:
            active = True
        return active

    @staticmethod
    def stored_filters():
        tool = getUtility(ICourseFilterTool)
        return tool.get()

    def active_filters(self):
        stored_data = self.stored_filters()
        if 'course-filter' in stored_data:
            filter_data = stored_data['course-filter']
            if 'filter' in filter_data:
                active_filters = dict()
                filters = filter_data['filter']
                for key, value in filters.items():
                    if key != 'token':
                        active_filters[key] = value
                return active_filters
            else:
                return None

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

    def has_active_session(self):
        active = False
        try:
            session = self.stored_filters()
        except KeyError:
            session = None
        if session:
            active = True
        return active

    @staticmethod
    def stored_filters():
        tool = getUtility(ICourseFilterTool)
        return tool.get()

    def is_selected_option(self, filter_value):
        if self.has_active_session():
            filter_data = self.stored_filters()['course-filter']
            try:
                active_filters = filter_data['filter']
            except KeyError:
                return False
            if filter_value in active_filters.values():
                return True
        return False

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

    def course_types(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.lectures.CourseType')
        course_types = dict()
        for term in vocab:
            course_types[term.value] = term.title
        return course_types

    @staticmethod
    def course_core_themes():
        return vocabulary.course_core_themes()

    def field_data_map(self):
        degree_courses = self.degree_courses()
        courses = {}
        for key, value in degree_courses.items():
            courses[value] = self.get_degree_course_title(value)
        field_map = {
            'courses': courses,
            'modules-ba': self.learning_modules_bachelor(),
            'modules-ma': self.learning_modules_master(),
            'core-themes': self.course_core_themes(),
            'course-types': self.course_types()
        }
        for theme_key, theme_value in self.course_core_themes().items():
            map_key = 'core-theme-{0}'.format(theme_key)
            field_map[map_key] = theme_value
        return field_map


class CourseFilterStorageInfo(BrowserView):

    def __call__(self):
        return self.render()

    @staticmethod
    def get_session_data():
        tool = getUtility(ICourseFilterTool)
        data = tool.get()
        return data

    def render(self):
        data = self.get_session_data()
        return json.dumps(data)


class CourseFilterStorageReset(BrowserView):

    def __call__(self):
        return self.render()

    def render(self):
        context = aq_inner(self.context)
        tool = getUtility(ICourseFilterTool)
        session = tool.get()
        session_data = session['course-filter']
        session_data['filters'] = list()
        tool.add('course-filter', session_data)
        api.portal.show_message(
            message=_(u"Session reset"), request=self.request)
        return self.request.response.redirect(context.absolute_url())


class CourseFilterStorageCleanup(BrowserView):

    def __call__(self):
        return self.render()

    def render(self):
        context = aq_inner(self.context)
        tool = getUtility(ICourseFilterTool)
        tool.destroy()
        api.portal.show_message(
            message=_(u"Session cleared"), request=self.request)
        return self.request.response.redirect(context.absolute_url())
