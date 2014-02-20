from five import grok
from zope import schema

from plone.dexterity.content import Container
from plone.directives import form
from plone.app.textfield import RichText
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from hph.faculty import MessageFactory as _


class IFacultyMember(form.Schema, IImageScaleTraversable):
    """
    A faculty staff member
    """
    last_name = schema.TextLine(
        title=_(u"Lastname"),
        description=_(u"Provide last name for better filtering and search"),
        required=True,
    )
    form.widget(position=CheckBoxFieldWidget)
    position = schema.Set(
        title=_(u"Medium"),
        value_type=schema.Choice(
            title=_(u"Accademic Role or Position"),
            vocabulary=u'hph.faculty.FacultyMemberPosition',
        ),
        required=True,
    )
    sidenote = schema.TextLine(
        title=_(u"Sidenote"),
        description=_(u"Optional additional information/sidenote"),
        required=False,
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
        title=_(u"Portrait Image"),
        required=False,
    )
    text = RichText(
        title=_(u"Body Text"),
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
