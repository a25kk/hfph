# -*- coding: utf-8 -*-
"""Module providing faculty member assignment functionality"""
from Acquisition import aq_inner
from plone import api
from plone.protect.utils import addTokenToUrl
from Products.Five.browser import BrowserView
from zope.lifecycleevent import modified
from zope.publisher.interfaces.browser import IPublishTraverse
from zope.interface import implementer

from hph.faculty.facultymember import IFacultyMember

from hph.publications import MessageFactory as _


class FacultyMemberAssignment(BrowserView):
    """ Manage publication faculty member assignments """

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

    def generate_protected_url(self, url):
        return addTokenToUrl(url)

    def selectable_faculty_members(self):
        faculty_members = api.content.find(
            context=api.portal.get(),
            object_provides=IFacultyMember,
            review_state='published',
            sort_on='lastname'
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


@implementer(IPublishTraverse)
class FacultyMemberAssignmentFactory(BrowserView):
    """ Factory view to set and delete assignments """

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
        faculty_member_uid = self.traverse_subpath[0]
        action = self.traverse_subpath[1]
        faculty_member = api.content.get(UID=faculty_member_uid)
        assignments = getattr(faculty_member, 'associatedPublications', None)
        if assignments is None:
            assignments = list()
        uuid = api.content.get_uuid(obj=context)
        if action == 'remove':
            if uuid in assignments:
                assignments.remove(uuid)
        else:
            assignments.append(uuid)
        # Store updated assignment list
        setattr(faculty_member, 'associatedPublications', assignments)
        modified(faculty_member)
        faculty_member.reindexObject(idxs='modified')
        next_url = '{0}/@@faculty-member-assignment?updated=true'.format(
            context.absolute_url())
        api.portal.show_message(
            message=_(u"Faculty member successfully assigned"),
            request=self.request)
        return self.request.response.redirect(next_url)
