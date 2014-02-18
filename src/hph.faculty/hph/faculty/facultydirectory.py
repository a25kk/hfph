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


# Interface class; used to define content-type schema.

class IFacultyDirectory(form.Schema, IImageScaleTraversable):
    """
    A directory of faculty staff members
    """


class FacultyDirectory(Container):
    grok.implements(IFacultyDirectory)


class View(grok.View):
    """ Faculty staff listing with role filter """

    grok.context(IFacultyDirectory)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.filter = self.request.get('content_filter', '')

    def filtered(self):
        return self.filter is True
