# -*- coding: utf-8 -*-
"""Module providing faculty member assignment functionality"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api

from hph.faculty.facultymember import IFacultyMember


class FacultyMemberAssignment(BrowserView):
    """ Edit course module data via basic form """

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
        return self.index()#

    def selectable_faculty_members(self):
        faculty_members = api.content.find(
            context=api.portal.get(),
            object_provides=IFacultyMember,
            review_state='published'
        )
        return faculty_members

    def has_active_assignment(self, uuid):
        context = aq_inner(self.context)
        context_uid = api.content.get_uuid(obj=context)
        faculty_member = api.content.get(UID=uuid)
        assignments = getattr(faculty_member, 'associatedPublications', None)
        if assignments and context_uid in assignments:
            return True
        return False


class FacultyMemberAssign(BrowserView):
    """ Edit course module data via basic form """

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
        return self.index()
