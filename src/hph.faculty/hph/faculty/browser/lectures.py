# -*- coding: utf-8 -*-
"""Module providing definitions"""
from AccessControl import Unauthorized
from Acquisition import aq_inner, aq_parent
from Products.Five import BrowserView
from hph.lectures.coursefolder import ICourseFolder
from hph.lectures.lecture import ILecture
from plone import api
from zc.relation.interfaces import ICatalog
from zope.component import queryUtility
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from plone.app.linkintegrity.handlers import referencedRelationship
from zope.schema.vocabulary import getVocabularyRegistry


class CourseView(BrowserView):
    """ Course default view """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.has_lectures = len(self.available_lectures()) > 0
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def rendered_course_card(uuid):
        context = api.content.get(UID=uuid)
        template = context.restrictedTraverse('@@course-card')(
            preview=True
        )
        return template

    @staticmethod
    def get_current_course_folder():
        catalog = api.portal.get_tool(name='portal_catalog')
        sub_folders = catalog(object_provides=ICourseFolder.__identifier__,
                              review_state='published')
        for folder in sub_folders:
            container = folder.getObject()
            current_marker = getattr(container, 'is_current_semester', None)
            if current_marker:
                return folder
        return sub_folders[0]

    def available_lectures(self):
        course_folder = self.get_current_course_folder()
        obj_provides = ILecture.__identifier__
        query = dict(object_provides=obj_provides,
                     path=dict(query=course_folder.getPath(),
                               depth=1),
                     review_state='published',
                     sort_on='courseNumber')
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(query)
        return results

    def related_lecturers(self, obj):
        """Returns a list of brains of related items."""
        results = []
        course = obj.getObject()
        catalog = api.portal.get_tool('portal_catalog')
        for rel in course.lecturer:
            if rel.isBroken():
                # skip broken relations
                continue
            # query by path so we don't have to wake up any objects
            try:
                brains = catalog(path={'query': rel.to_path, 'depth': 0})
                results.append(brains[0])
            except Unauthorized:
                print(rel.from_object.Title)
                pass
        return results

    def lecture_data(self):
        context = aq_inner(self.context)
        context_uid = context.UID()
        courses = self.available_lectures()
        course_list = list()
        for course in courses:
            lecturers = [
                lecturer.UID for lecturer in self.related_lecturers(course)
            ]
            if context_uid in lecturers:
                course_list.append(course.UID)
        return course_list

    def related_courses(self):
        courses = self.lecture_data()
        return courses

    def parent_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def computed_klass(self, value):
        context = aq_inner(self.context)
        active_filter = getattr(context, 'academicRole', None)
        klass = 'app-nav-list-item'
        if active_filter == value:
            klass += 'app-nav-list-item-active'
        return klass
