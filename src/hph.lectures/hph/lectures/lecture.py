# -*- coding: utf-8 -*-
"""Module providing lecture content"""
from Acquisition import aq_inner
from five import grok
from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.widgets.dx import RelatedItemsWidget
from plone.dexterity.content import Container
from plone.directives import form
from plone.indexer import indexer
from plone.namedfile.interfaces import IImageScaleTraversable
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.schema.vocabulary import getVocabularyRegistry

from hph.lectures import MessageFactory as _


class ILecture(form.Schema, IImageScaleTraversable):
    """
    A single course
    """
    subtitle = schema.TextLine(
        title=_(u"Subtitle"),
        required=False,
    )
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    courseNumber = schema.TextLine(
        title=_(u"Lecure Number"),
        required=True,
    )
    attendance = schema.TextLine(
        title=_(u"Attendance"),
        required=False,
    )
    attendanceRequired = schema.Bool(
        title=_(u"Attendance Required"),
        required=False,
    )
    blockLecture = schema.Bool(
        title=_(u"Block Lecture"),
        required=False,
    )
    description = schema.Text(
        title=_(u"Additional Information"),
        required=False,
    )
    form.widget('lecturer', RelatedItemsWidget)
    lecturer = RelationList(
        title=u"Lecturers",
        description=_(u"Please select one or more lecturers for this course"),
        default=[],
        value_type=RelationChoice(
            title=_(u"Related lecturer"),
            source=CatalogSource(portal_type='hph.faculty.facultymember'),
        ),
        required=False,
    )
    lecturerAdditional = schema.TextLine(
        title=_(u"Additional Lecturer"),
        required=False,
    )
    courseType = schema.Choice(
        title=_(u"Course Type"),
        description=_(u"Please select the course type."),
        required=False,
        vocabulary=u'hph.lectures.CourseType',
    )
    courseDuration = schema.Choice(
        title=_(u"Course Duration"),
        required=False,
        vocabulary=u'hph.lectures.CourseDuration',
    )
    courseDates = schema.TextLine(
        title=_(u"Course Dates"),
        required=True,
    )
    courseTime = schema.TextLine(
        title=_(u"Course Time"),
        required=True,
    )
    courseSemester = schema.Choice(
        title=_(u"Course Semester"),
        description=_(u"Please select the course semester for filtering"),
        required=True,
        vocabulary=u'hph.lectures.CourseSemester',
    )
    courseYear = schema.TextLine(
        title=_(u"Course Year"),
        required=True,
    )
    courseRoom = schema.TextLine(
        title=_(u"Course Room"),
        required=False,
    )
    form.widget(thirdPartyProject=CheckBoxFieldWidget)
    thirdPartyProject = schema.Set(
        title=_(u"Third Party Project Display"),
        value_type=schema.Choice(
            title=_(u"Display Selection"),
            vocabulary=u'hph.sitecontent.thirdPartyProjects',
        ),
        required=False,
    )


@indexer(ILecture)
def courseTypeIndexer(obj):
    return obj.courseType
grok.global_adapter(courseTypeIndexer, name="courseType")


@indexer(ILecture)
def thirdPartyProjectIndexer(obj):
    return obj.thirdPartyProject
grok.global_adapter(thirdPartyProjectIndexer, name="thirdPartyProject")


class Lecture(Container):
    grok.implements(ILecture)
    pass


class View(grok.View):
    grok.context(ILecture)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.anon = self.is_anon()
        self.has_attachments = len(self.attachments()) > 0

    def is_anon(self):
        return api.user.is_anonymous()

    def attachments(self):
        context = aq_inner(self.context)
        items = context.restrictedTraverse('@@folderListing')(
            portal_type=['File'])
        return items

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

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.lectures.CourseType')
        return vocab

    def computed_klass(self, value):
        context = aq_inner(self.context)
        active_filter = getattr(context, 'courseType', None)
        klass = 'nav-item-plain'
        if active_filter == value:
            klass = 'active'
        return klass
