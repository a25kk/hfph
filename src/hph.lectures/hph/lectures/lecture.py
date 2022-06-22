# -*- coding: utf-8 -*-
"""Module providing lecture content"""
from Acquisition import aq_inner
# # from five import grok
from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsWidget
from plone.autoform import directives as form, directives
from plone.dexterity.browser import edit
from plone.dexterity.content import Container
from plone.indexer import indexer
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.schema.vocabulary import getVocabularyRegistry
from zope.component import getUtility
from zope.interface import implementer

from hph.lectures.interfaces import ICourseModuleTool

from hph.lectures import MessageFactory as _


class ILecture(model.Schema, IImageScaleTraversable):
    """
    A single course
    """
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
        description=_(u"Please enter the prefix that you want to be "
                      u"displayed as well, e.g. additional lecturer"),
        required=False,
    )
    courseType = schema.Choice(
        title=_(u"Course Type"),
        description=_(u"Please select the course type."),
        required=False,
        vocabulary=u'hph.lectures.CourseType',
    )
    title = schema.TextLine(
        title=_(u"Course Title"),
        required=True,
    )
    courseNumber = schema.TextLine(
        title=_(u"Lecure Number"),
        required=True,
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
    courseRoom = schema.TextLine(
        title=_(u"Course Room"),
        required=False,
    )
    courseRegistration = schema.TextLine(
        title=_(u"Course registration required"),
        description=_(u"(Example: register until 19.01.2017 via example.tld)"),
        required=False
    )
    courseRestricted = schema.TextLine(
        title=_(u"Course participation restricted"),
        description=_(u"(Example 1: maximum participants 12)"
                      u"(Example 2: Participation only for students of the "
                      u"ethics master)"
                      ),
        required=False
    )
    blockLecture = schema.Bool(
        title=_(u"Block Lecture"),
        required=False,
    )
    onlineLecture = schema.Bool(
        title=_(u"Online Lecture"),
        required=False,
    )
    proPhilosophiaExtra = schema.Bool(
        title=_(u"pro‐philosophia‐extra"),
        required=False,
    )
    courseCancelled = schema.Bool(
        title=_(u"Course cancelled"),
        required=False,
    )
    description = schema.Text(
        title=_(u"Additional Information"),
        required=False,
    )
    moodle = schema.TextLine(
        title=_(u"Moodle Link"),
        description=_(u"Please enter absolute link to moodle representation"),
        required=False,
    )
    form.widget(externalFundsProject=CheckBoxFieldWidget)
    externalFundsProject = schema.List(
        title=_(u"Third Party Project Display"),
        value_type=schema.Choice(
            title=_(u"Display Selection"),
            vocabulary=u'hph.sitecontent.thirdPartyProjects',
        ),
        required=False,
    )
    form.widget(moduleStudies=CheckBoxFieldWidget)
    moduleStudies = schema.List(
        title=_(u"Module Studies Recommendations"),
        value_type=schema.Choice(
            title=_(u"Display Selection"),
            vocabulary=u'hph.lectures.vocabulary.moduleStudies',
        ),
        required=False,
    )

    # Omitted fields
    # TODO: remove after browser view cleanup
    directives.omitted('courseTime')
    courseTime = schema.TextLine(
        title=_(u"Course Time"),
        required=True,
    )
    directives.omitted('courseSemester')
    courseSemester = schema.Choice(
        title=_(u"Course Semester"),
        description=_(u"Please select the course semester for filtering"),
        required=True,
        vocabulary=u'hph.lectures.CourseSemester',
    )
    directives.omitted('courseYear')
    courseYear = schema.TextLine(
        title=_(u"Course Year"),
        required=True,
    )

@indexer(ILecture)
def courseTypeIndexer(obj):
    return obj.courseType
grok.global_adapter(courseTypeIndexer, name="courseType")


@indexer(ILecture)
def externalFundsProjectIndexer(obj):
    return obj.externalFundsProject
grok.global_adapter(externalFundsProjectIndexer, name="externalFundsProject")


@implementer(ILecture)
class Lecture(Container):
    pass


class EditForm(edit.DefaultEditForm):
    """Custom edit form overriding date grid widget settings"""

    def update_widget_settings(self, widget_name, widgets):
        widget = widgets[widget_name]
        widget.allow_insert = True
        widget.allow_delete = True
        widget.auto_append = True
        widget.allow_reorder = False

    def course_module_data_grid(self):
        data_grid_widget = 'ICourseModuleInformation.moduledetails'
        for group in self.groups:
            group_widgets = group.widgets
            if data_grid_widget in group_widgets:
                self.update_widget_settings(data_grid_widget, group_widgets)

    def update(self):
        super(EditForm, self).update()
        self.course_module_data_grid()


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
        klass = 'app-nav-list-item app-nav-list-item-plain'
        if active_filter == value:
            klass = 'app-nav-list-item app-nav-list-item-active'
        return klass

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
