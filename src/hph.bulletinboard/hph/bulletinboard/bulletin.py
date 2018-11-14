from five import grok
from plone.directives import dexterity, form

from plone.app.textfield import RichText

from hph.bulletinboard import MessageFactory as _


class IBulletin(form.Schema):
    """
    A single bulletin or announcement
    """
    text = RichText(
        title=_(u"Text"),
        required=False
    )


class Bulletin(dexterity.Item):
    grok.implements(IBulletin)


class View(grok.View):
    grok.context(IBulletin)
    grok.require('zope2.View')
    grok.name('view')
