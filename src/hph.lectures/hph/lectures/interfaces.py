# -*- coding: UTF-8 -*-
"""Lecture edit form schema interfaces"""

from plone.directives import form
from zope import schema
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.theme.interfaces import IDefaultPloneLayer
from plone.namedfile.field import NamedBlobFile

from hph.lectures import MessageFactory as _


class IHPHLecturesLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class ICourseModuleTool(Interface):
    """ Course module data processing

        General tool providing CRUD operations for assigning modules
        to lecture content objects
    """

    def create(context):
        """ Create asset assignment data file

        The caller is responsible for passing a valid data dictionary
        containing the necessary details

        Returns JSON object

        @param uuid:        content object UID
        @param data:        predefined initial data dictionary
        """

    def read(context):
        """ Read stored data from object

        Returns a dictionary

        @param uuid:        object UID
        @param key:         (optional) dictionary item key
        """

    def update(context):
        """ Update stored data from object

        Returns a dictionary

        @param uuid:        object UID
        @param key:         (optional) dictionary item key
        @param data:        data dictionary
        """

    def delete(context):
        """ Delete stored data from object

        Returns a dictionary

        @param uuid:        caravan site object UID
        @param key:         (optional) dictionary item key
        """


class ILectureBase(form.Schema):
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
    onlineLecture = schema.Bool(
        title=_(u"Online Lecture"),
        required=False,
    )
    description = schema.Text(
        title=_(u"Additional Information"),
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


class ILectureAttachment(form.Schema):
    """Schema for attachment handling"""

    title = schema.TextLine(
        title=_(u"Title"),
        required=True
    )
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )
    image = NamedBlobFile(
        title=_(u"File Attachment"),
        description=_(u"Select file to upload to this lecture object"),
        required=False,
    )
