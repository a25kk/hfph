from Acquisition import aq_inner
from five import grok
from plone import api

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import getVocabularyRegistry

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from collective.z3cform.widgets.token_input_widget import TokenInputFieldWidget

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
    form.widget('lecturer', AutocompleteMultiFieldWidget)
    lecturer = RelationList(
        title=u"Lecturers",
        description=_(u"Please select one or more lecturers for this course"),
        default=[],
        value_type=RelationChoice(
            title=_(u"Related lecturer"),
            source=ObjPathSourceBinder(
                object_provides=IFacultyMember.__identifier__)
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
    form.widget(courseRoom=TokenInputFieldWidget)
    courseRoom = schema.List(
        title=_(u"Course Room"),
        required=False,
        value_type=schema.TextLine(),
        default=[],
    )
    form.widget(thirdPartyProject=CheckBoxFieldWidget)
    thirdPartyProject = schema.Set(
        title=_(u"Third Party Project Display"),
        value_type=schema.Choice(
            title=_(u"Display Selection"),
            vocabulary=u'hph.sitecontent.thirdPartyProjects',
        ),
        required=True,
    )


class Lecture(Container):
    grok.implements(ILecture)
    pass


class View(grok.View):
    grok.context(ILecture)
    grok.require('zope2.View')
    grok.name('view')

    def can_edit(self):
        if api.user.is_anonymous():
            return False
        allowed = False
        context = aq_inner(self.context)
        user = api.user.get_current()
        perms = api.user.get_permissions(username=user, obj=context)
        if 'cmf.ModifyPortalContent' in perms:
            allowed = True
        return allowed

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
