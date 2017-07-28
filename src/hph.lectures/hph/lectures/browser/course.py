# -*- coding: utf-8 -*-
"""Module providing lecture views"""
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from hph.lectures.interfaces import ICourseModuleTool
from plone import api
from zope.component import getUtility
from zope.schema.vocabulary import getVocabularyRegistry

from hph.lectures import MessageFactory as _, vocabulary


class CourseView(BrowserView):
    """ Course default view """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.has_attachments = len(self.attachments()) > 0
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def is_anon():
        return api.user.is_anonymous()

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
            admin_roles = ('Manager', 'Site Administrator',
                           'StaffMember', 'Owner')
            roles = api.user.get_roles(username=user_id, obj=context)
            for role in roles:
                if role in admin_roles:
                    allowed = True
        return allowed

    def display_edit_notification(self):
        if api.user.is_anonymous():
            return False
        context = aq_inner(self.context)
        is_owner = False
        user = api.user.get_current()
        if user.getId() in context.listContributors():
            is_owner = True
        return is_owner

    def attachments(self):
        context = aq_inner(self.context)
        items = context.restrictedTraverse('@@contentlisting')(
            portal_type=['File'])
        return items

    @staticmethod
    def rendered_course_card(uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse('@@course-card')(
            preview=False
        )
        return template

    def course_information(self):
        context = aq_inner(self.context)
        context_uid = api.content.get_uuid(obj=context)
        tool = getUtility(ICourseModuleTool)
        data = tool.read(context_uid)
        return data

    def has_course_information(self):
        if self.course_information():
            return True
        return False

    def module_data(self):
        stored_data = self.course_information()
        data = dict()
        for item in stored_data['items']:
            if 'degree-course' in item:
                course_identifier = item['degree-course']
                try:
                    course_module = item['module']
                except KeyError:
                    course_module = None
                course_theme = None
                if 'course-theme' in item:
                    course_theme = item['course-theme']
                if course_identifier in data:
                    course_data = data[course_identifier]
                else:
                    # Add empty dictionary if course identifier
                    # does not yet exist
                    course_data = {}
                if course_module:
                    if course_module in course_data:
                        module_info = course_data[course_module]
                    else:
                        module_info = list()
                    if course_theme:
                        module_info.append(course_theme)
                    course_data[course_module] = module_info
                data[course_identifier] = course_data
        return data

    def module_index_data(self):
        stored_data = self.course_information()
        storage_blacklist = ('degree', 'info', 'theme')
        data = list()
        for item in stored_data['items']:
            if 'degree-course' in item:
                for key, value in item.items():
                    if key not in storage_blacklist:
                        if key == 'degree-course':
                            value = self.get_degree_course_title(value)
                        # if value not in data:
                        data.append(value)
        # Remove possible duplicates
        module_data = list(set(data))
        return module_data

    @staticmethod
    def get_degree_course_title(course):
        course_names = vocabulary.degree_courses_tokens()
        return course_names[course]

    @staticmethod
    def get_learning_modules(course, course_module):
        if course == 'ba':
            modules = vocabulary.learning_modules_bachelor()
        else:
            modules = vocabulary.learning_modules_master()
        try:
            module_title = modules[course_module]
        except KeyError:
            module_title = course_module
        return module_title

    def has_module_data(self):
        return len(self.module_data()) > 0

    def course_filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.lectures.CourseType')
        return vocab

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

    def computed_class(self, value):
        context = aq_inner(self.context)
        active_filter = getattr(context, 'courseType', None)
        css_class = 'app-nav-list-item app-nav-list-item-plain'
        if active_filter == value:
            css_class = 'app-nav-list-item app-nav-list-item-active'
        return css_class


class CoursePreview(BrowserView):
    """ Embeddable course preview snippet """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, preview=False, **kw):
        self.is_preview_card = preview
        return self.render()

    def render(self):
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
            admin_roles = ('Manager', 'Site Administrator',
                           'StaffMember', 'Owner')
            roles = api.user.get_roles(username=user_id, obj=context)
            for role in roles:
                if role in admin_roles:
                    allowed = True
        return allowed

    def course_information(self):
        context = aq_inner(self.context)
        context_uid = api.content.get_uuid(obj=context)
        tool = getUtility(ICourseModuleTool)
        data = tool.read(context_uid)
        return data

    def has_course_information(self):
        if self.course_information():
            return True
        return False

    def module_data(self):
        stored_data = self.course_information()
        data = dict()
        for item in stored_data['items']:
            if 'degree-course' in item:
                course_identifier = item['degree-course']
                try:
                    course_module = item['module']
                except KeyError:
                    course_module = None
                course_theme = None
                if 'course-theme' in item:
                    course_theme = item['course-theme']
                if course_identifier in data:
                    course_data = data[course_identifier]
                else:
                    # Add empty dictionary if course identifier
                    # does not yet exist
                    course_data = {}
                if course_module:
                    if course_module in course_data:
                        module_info = course_data[course_module]
                    else:
                        module_info = list()
                    if course_theme:
                        module_info.append(course_theme)
                    course_data[course_module] = module_info
                data[course_identifier] = course_data
        return data

    @staticmethod
    def get_degree_course_title(course):
        course_names = vocabulary.degree_courses_tokens()
        return course_names[course]

    @staticmethod
    def get_learning_modules(course, module):
        if course == 'ba':
            modules = vocabulary.learning_modules_bachelor()
        else:
            modules = vocabulary.learning_modules_master()
        try:
            module_title = modules[module]
        except KeyError:
            module_title = module
        return module_title

    def has_module_data(self):
        if self.module_data():
            return True
        return False

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
