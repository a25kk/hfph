from z3c.form import form
from plone.autoform.form import AutoExtensibleForm

from plone.app.textfield import RichText
from plone.supermodel import model
from plone.dexterity.content import Item
from zope.interface import implementer

from hph.bulletinboard import MessageFactory as _


class IBulletin(model.Schema):
    """
    A single bulletin or announcement
    """
    text = RichText(
        title=_(u"Text"),
        required=False
    )


@implementer(IBulletin)
class Bulletin(Item):
    pass


