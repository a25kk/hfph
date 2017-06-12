# -*- coding: utf-8 -*-
"""Module providing views for course module editing"""
import collections

from Acquisition import aq_inner
from AccessControl import Unauthorized
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from plone import api
from plone.protect.utils import addTokenToUrl
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.publisher.interfaces.browser import IPublishTraverse
from zope.interface import implementer

from hph.lectures import vocabulary
from hph.lectures.interfaces import ICourseModuleTool

from hph.lectures import MessageFactory as _


class CourseModuleEditor(BrowserView):
    """ Edit course module data via basic form """

    def __call__(self):
        self.errors = {}
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
                self.add_module_information(form_data)

    def render(self):
        self.update()
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

    def add_module_information(self, data):
        context = aq_inner(self.context)
        context_uid = api.content.get_uuid(obj=context)
        tool = getUtility(ICourseModuleTool)
        stored_data = tool.read(context_uid)
        if not stored_data:
            tool.create(context_uid, data)
        else:
            records = stored_data['items']
            if records:
                records.append(data)
                updated_records = records
            else:
                updated_records = [data]
            tool.update(context_uid, updated_records)
        next_url = '{0}/@@module-editor'.format(
            context.absolute_url()
        )
        return self.request.response.redirect(next_url)

    def generate_protected_url(self, url):
        return addTokenToUrl(url)


@implementer(IPublishTraverse)
class CourseModuleEditorRemove(BrowserView):
    """ Remove course module data """

    def __call__(self):
        return self.render()

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def render(self):
        context = aq_inner(self.context)
        authenticator = getMultiAdapter((context, self.request),
                                        name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized
        context_uid = api.content.get_uuid(obj=context)
        item_index_string = self.traverse_subpath[0]
        item_index = int(item_index_string)
        tool = getUtility(ICourseModuleTool)
        stored_data = tool.read(context_uid)
        updated_data = stored_data['items']
        del updated_data[item_index]
        tool.update(context_uid, updated_data)
        next_url = '{0}/@@module-editor?_authenticator={1}'.format(
            context.absolute_url(),
            authenticator.token()
        )
        api.portal.show_message(
            message=_(u"Course module successfully removed"),
            request=self.request)
        return self.request.response.redirect(next_url)
