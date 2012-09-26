from five import grok
from plone.directives import dexterity, form


class INewsFolder(form.Schema):
    """
    A folder acting as a collection for news items
    """


class NewsFolder(dexterity.Container):
    grok.implements(INewsFolder)


class View(grok.View):
    grok.context(INewsFolder)
    grok.require('zope2.View')
    grok.name('view')
