from five import grok
from plone.directives import dexterity, form


class IEventFolder(form.Schema):
    """
    A folder acting as a collection for events
    """


class EventFolder(dexterity.Container):
    grok.implements(IEventFolder)


class View(grok.View):
    grok.context(IEventFolder)
    grok.require('zope2.View')
    grok.name('view')
