from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from hph.sitecontent import MessageFactory as _


# Interface class; used to define content-type schema.

class INewsEntry(form.Schema, IImageScaleTraversable):
    """
    A news or announcement item
    """


class NewsEntry(dexterity.Container):
    grok.implements(INewsEntry)


class View(grok.View):
    grok.context(INewsEntry)
    grok.require('zope2.View')
    grok.name('view')
