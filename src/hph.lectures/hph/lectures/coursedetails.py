from zope import schema
from zope.interface import alsoProvides
from z3c.form import form

from plone.autoform.interfaces import IFormFieldProvider

from hph.lectures import MessageFactory as _


class ICourseDetails(form.Schema):
    """ Behavior interface providing course details """

    form.fieldset(
        'details',
        label=_(u"Course Details"),
        fields=['courseTheme', 'courseAims',
                'courseMethod', 'coursePrereq',
                'courseQualification', 'courseTarget',
                'courseLiterature', 'courseNotes']
    )
    courseTheme = schema.Text(
        title=_("Course Theme"),
        required=False,
    )
    courseAims = schema.Text(
        title=_("Course Aims"),
        required=False,
    )
    courseMethod = schema.Text(
        title=_("Course Method"),
        required=False,
    )
    coursePrereq = schema.Text(
        title=_("Course Prerequirements"),
        required=False,
    )
    courseQualification = schema.Text(
        title=_("Course Qualification"),
        required=False,
    )
    courseTarget = schema.Text(
        title=_("Course Target"),
        required=False,
    )
    courseLiterature = schema.Text(
        title=_("Course Literature"),
        required=False,
    )
    courseNotes = schema.Text(
        title=_("Course Notes"),
        required=False,
    )

alsoProvides(ICourseDetails, IFormFieldProvider)
