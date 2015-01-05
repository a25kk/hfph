# -*- coding: UTF-8 -*-
"""Lecture edit form schema interfaces"""

from plone.directives import form
from zope import schema
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.namedfile.field import NamedBlobFile

from hph.lectures import MessageFactory as _


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


class ILectureAttachement(form.Schema):

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
