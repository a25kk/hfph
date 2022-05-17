from five import grok
from z3c.form import form


class IEventFolder(form.Schema):
    """
    A folder acting as a collection for events
    """


class EventFolder(dexterity.Container):
    grok.implements(IEventFolder)

