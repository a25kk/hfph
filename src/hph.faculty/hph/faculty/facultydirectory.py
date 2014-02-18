from five import grok
from plone import api

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable

from hph.faculty import MessageFactory as _


class IFacultyDirectory(form.Schema, IImageScaleTraversable):
    """
    A directory of faculty staff members
    """


class FacultyDirectory(Container):
    grok.implements(IFacultyDirectory)


class View(grok.View):
    grok.context(IFacultyDirectory)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.filter = self.request.get('content_filter', '')

    def filtered(self):
        return self.filter is True
