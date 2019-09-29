from five import grok
from plone.directives import dexterity, form


class IEventFolder(form.Schema):
    """
    A folder acting as a collection for events
    """


class EventFolder(dexterity.Container):
    grok.implements(IEventFolder)

