# -*- coding: utf-8 -*-
"""Module providing course folder views"""
from plone import api

from Acquisition import aq_inner
from Products.Five import BrowserView


class CourseFolderView(BrowserView):
    """ Course folder default view """

    # TODO: Refactor to provide archive listing cards

    def __call__(self):
        self.has_archives = len(self.sub_folders()) > 0
        self.has_current_semester_container = False
        return self.render()

    def render(self):
        if self.has_archives:
            current_semester_folder = self.get_highlighted_container()
            next_url = current_semester_folder.getURL()
        else:
            context = aq_inner(self.context)
            next_url = '{0}/@@course-listing'.format(context.ansolute_url())
        return self.request.response.redirect(next_url)

    def sub_folders(self):
        context = aq_inner(self.context)
        folders = context.restrictedTraverse('@@folderListing')(
            portal_type='hph.lectures.coursefolder',
            review_state='published')
        return folders

    def get_highlighted_container(self):
        sub_folders = self.sub_folders()
        import pdb; pdb.set_trace()
        for folder in sub_folders:
            container = folder.getObject()
            current_marker = getattr(container, 'is_current_semester', None)
            if current_marker:
                return folder
        return sub_folders[0]

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
