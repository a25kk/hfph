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


from hph.faculty import MessageFactory as _

display = SimpleVocabulary(
    [SimpleTerm(value=u'lecturer', title=_(u'Lecturer')),
     SimpleTerm(value=u'professor', title=_(u'Professor')),
     SimpleTerm(value=u'docent', title=_(u'Docent'))]
)


class IFacultyMember(form.Schema, IImageScaleTraversable):
    """
    A faculty staff member
    """
    last_name = schema.TextLine(
        title=_(u"Lastname"),
        description=_(u"Provide last name for better filtering and search"),
        required=True,
    )
    department = schema.TextLine(
        title=_(u"Department"),
        required=True,
    )
    street = schema.TextLine(
        title=_(u"Street"),
        required=True,
    )
    city = schema.TextLine(
        title=_(u"City"),
        required=True,
    )
    phone = schema.TextLine(
        title=_(u"Phone"),
        required=True,
    )
    fax = schema.TextLine(
        title=_(u"Fax"),
        required=True,
    )
    email = schema.TextLine(
        title=_(u"E-Mail"),
        required=True,
    )
    image = NamedBlobImage(
        title=-(u"Portrait Image"),
        required=False,
    )


class FacultyMember(Container):
    grok.implements(IFacultyMember)


class View(grok.View):
    """ Faculty member view """

    grok.context(IFacultyMember)
    grok.require('zope2.View')
    grok.name('view')

    # Add view methods here
