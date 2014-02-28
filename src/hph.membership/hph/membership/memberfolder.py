from five import grok

from plone.directives import form
from plone.dexterity.content import Container
from plone.namedfile.interfaces import IImageScaleTraversable


class IMemberFolder(form.Schema, IImageScaleTraversable):
    """
    Container for member workspaces
    """


class MemberFolder(Container):
    grok.implements(IMemberFolder)
    pass


class View(grok.View):
    grok.context(IMemberFolder)
    grok.require('zope2.View')
    grok.name('view')
