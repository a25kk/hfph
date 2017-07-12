# -*- coding: utf-8 -*-
"""Module providing lecture views"""
from Acquisition import aq_inner
from Products.Five import BrowserView
from bpython.translations import _
from hph.lectures.interfaces import ICourseModuleTool
from plone import api
from zope.component import getUtility
from zope.schema.vocabulary import getVocabularyRegistry

from hph.lectures import MessageFactory as _


class CourseView(BrowserView):
    """ Course default view """

    def __init__(self, context, request):
        self.context = context
        self.request = request


class CoursePreview(BrowserView):
    """ Embeddable course preview snippet """

    def __init__(self, context, request):
        self.context = context
        self.request = request

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
