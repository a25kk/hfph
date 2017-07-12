# -*- coding: utf-8 -*-
"""Module providing course listings"""
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from plone import api

from hph.lectures import MessageFactory as _
from zope.component import getMultiAdapter
from zope.schema.vocabulary import getVocabularyRegistry


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

    def filter_courses(self, data):
        return
