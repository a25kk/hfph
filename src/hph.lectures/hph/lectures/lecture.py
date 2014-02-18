from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget

from hph.faculty.facultymember import IFacultyMember

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
    attendanceRequired = schema.Bool(
        title=_(u"Attendance Required"),
        required=False,
    )
    description = schema.Text(
        title=_(u"Additional Information"),
        required=False,
    )
    form.widget('lecturer', AutocompleteMultiFieldWidget)
    lecturer = RelationList(
        title=u"Lecturers",
        description=_(u"Please select one or more lecturers for this course"),
        default=[],
        value_type=RelationChoice(
            title=_(u"Related lecturer"),
            source=ObjPathSourceBinder(
                object_provides=IFacultyMember.__identifier__,
            )
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


class Lecture(Container):
    grok.implements(ILecture)
    pass


class View(grok.View):
    grok.context(ILecture)
    grok.require('zope2.View')
    grok.name('view')
