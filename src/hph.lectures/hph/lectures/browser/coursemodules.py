# -*- coding: utf-8 -*-
"""Module providing views for course module editing"""
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from plone import api
from zope.component import getUtility
from zope.component import getMultiAdapter

from hph.lectures.interfaces import ICourseModuleTool


class CourseModuleEditor(BrowserView):
    """ Edit course module data via basic form """

    def __call__(self):
        self.errors = {}
        return self.render()

    def update(self):
        translation_service = api.portal.get_tool(name="translation_service")
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('degree', 'info')
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
            tool.update(context_uid, data)
        next_url = '{0}/@@module-editor'.format(
            context.absolute_url()
        )
        return self.request.response.redirect(next_url)
