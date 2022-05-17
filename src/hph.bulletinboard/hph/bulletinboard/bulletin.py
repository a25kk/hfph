from five import grok

from z3c.form import form
from plone.autoform.form import AutoExtensibleForm

from plone.app.textfield import RichText

from hph.bulletinboard import MessageFactory as _


class IBulletin(AutoExtensibleForm, form.Form):
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
