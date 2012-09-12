from five import grok
from Acquisition import aq_inner
from plone.directives import dexterity, form

from Products.CMFCore.utils import getToolByName

from plone.app.contentlisting.interfaces import IContentListing
from hph.bulletinboard.bulletin import IBulletin

from hph.bulletinboard import MessageFactory as _


class IBulletinBoard(form.Schema):
    """
    A bulletin board holding announcements
    """


class BulletinBoard(dexterity.Container):
    grok.implements(IBulletinBoard)


class View(grok.View):
    grok.context(IBulletinBoard)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_bulletins = len(self.contained_bulletins()) > 0

    def contained_bulletins(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IBulletin.__identifier__,
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist
