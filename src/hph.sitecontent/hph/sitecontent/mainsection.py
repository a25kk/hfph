from five import grok
from plone.directives import dexterity, form

from zope import schema

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from hph.sitecontent import MessageFactory as _


class IMainSection(form.Schema, IImageScaleTraversable):
    """
    Forder to represent the main site sections
    """


class MainSection(dexterity.Container):
    grok.implements(IMainSection)


class View(grok.View):
    grok.context(IMainSection)
    grok.require('zope2.View')
    grok.name('view')
