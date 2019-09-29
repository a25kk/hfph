# -*- coding: utf-8 -*-
"""Module providing a custom indexing setup for site content"""
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from plone import api
from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.textfield.value import IRichTextValue
from plone.indexer.decorator import indexer
from zope.component import getUtility

from hph.lectures import vocabulary
from hph.lectures.interfaces import ICourseFilterTool
from hph.lectures.interfaces import ICourseModuleTool
from hph.lectures.lecture import ILecture


def _unicode_save_string_concat(*args):
    """ Concat args and return utf-8 strings
        Operates independent of input format (unicode or str)
    """
    result = ''
    for value in args:
        if isinstance(value, unicode):
            value = value.encode('utf-8', 'replace')
        result = ' '.join((result, value))
    return result


def SearchableText(obj):
    text = u""
    rich_text = IRichText(obj, None)
    if rich_text:
        text_value = rich_text.text
        if IRichTextValue.providedBy(text_value):
            transforms = getToolByName(obj, 'portal_transforms')
            text = transforms.convertTo(
                'text/plain',
                safe_unicode(text_value.output).encode('utf8'),
                mimetype=text_value.mimeType,
            ).getData().strip()

    subject = u' '.join(
        [safe_unicode(s) for s in obj.Subject()]
    )

    return u" ".join((
        safe_unicode(obj.id),
        safe_unicode(obj.title) or u"",
        safe_unicode(obj.description) or u"",
        safe_unicode(text),
        safe_unicode(subject),
    ))


def get_course_information(obj):
    context = aq_inner(obj)
    context_uid = api.content.get_uuid(obj=context)
    tool = getUtility(ICourseModuleTool)
    data = tool.read(context_uid)
    return data


def get_degree_course_title(course):
    course_names = vocabulary.degree_courses_tokens()
    return course_names[course]


def course_module_information(obj):
    context = aq_inner(obj)
    context_uid = api.content.get_uuid(obj=context)
    tool = getUtility(ICourseModuleTool)
    data = tool.get_record_index(context_uid)
    return data


@indexer(ILecture)
def index_lecture_course_modules(obj):
    course_information = course_module_information(obj)
    indexed_data = tuple(safe_unicode(s.strip()) for s in course_information)
    return indexed_data
