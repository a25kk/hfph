# from five import grok
from zope.interface import implementer

from plone.dexterity.content import Container
from plone.supermodel import model

from z3c.form import form


class IEventFolder(model.Schema):
    """
    A folder acting as a collection for events
    """


@implementer(IEventFolder)
class EventFolder(Container):
    pass
