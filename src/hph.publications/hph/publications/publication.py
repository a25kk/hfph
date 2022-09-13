# -*- coding: UTF-8 -*-
from zope import schema
from zope.interface import implementer

# from five import grok
from plone import api
from plone.app.textfield import RichText
from plone.autoform import directives as form
#from z3c.form import form
from plone.dexterity.content import Item
from plone.indexer import indexer
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model

from Acquisition import aq_inner
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from hph.publications import MessageFactory as _


class IPublication(model.Schema, IImageScaleTraversable):
    """
    A single publication like a book, dvd or magazine
    """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    publicationYear = schema.TextLine(
        title=_(u"Year of Publication"),
        required=True,
    )
    editor = schema.Bool(
        title=_(u"Editor"),
        required=True,
    )
    lastname = schema.TextLine(
        title=_(u"Author Lastname"),
        description=_(u"The entered value will be used to associate this "
                      u"publication with the corresponding faculty member"),
        required=True,
    )
    authorOne = schema.TextLine(
        title=_(u"Author One"),
        required=True,
    )
    authorTwo = schema.TextLine(
        title=_(u"Author Two"),
        required=False,
    )
    authorThree = schema.TextLine(
        title=_(u"Author Three"),
        required=False,
    )
    authorPlus = schema.Bool(
        title=_(u"More Authors"),
        required=False,
    )
    media = schema.Choice(
        title=_(u"Medium"),
        description=_(u"This is the field publications can be filtered on"),
        vocabulary=u"hph.publications.publicationMedia",
        required=False,
    )
    bookSeries = schema.Choice(
        title=_(u"Series"),
        description=_(u"This is the field publications can be filtered on"),
        vocabulary=u'hph.publications.publicationSeries',
        required=False,
    )
    form.widget(externalFundsProject=CheckBoxFieldWidget)
    externalFundsProject = schema.List(
        title=_(u"Third Party Project Display"),
        value_type=schema.Choice(
            title=_(u"Display Selection"),
            vocabulary=u'hph.sitecontent.thirdPartyProjects',
        ),
        required=False,
    )
    summary = RichText(
        title=_(u"Summary"),
        required=False,
    )
    image = NamedBlobImage(
        title=_(u"Cover Image"),
        description=_(u"Please upload a cover image"),
        required=False,
    )


@implementer(IPublication)
class Publication(Item):
    pass


class View(object):

    def item_contributor(self):
        if api.user.is_anonymous():
            return False
        context = aq_inner(self.context)
        is_owner = False
        user = api.user.get_current()
        if user.getId() in context.listContributors():
            is_owner = True
        return is_owner
