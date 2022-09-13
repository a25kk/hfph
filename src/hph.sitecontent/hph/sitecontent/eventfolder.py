# from five import grok
from z3c.form import form
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IEventFolder(model.Schema):
    """
    A folder acting as a collection for events
    """


@implementer(IEventFolder)
class EventFolder(Container):
    pass
