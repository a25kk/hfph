from five import grok
from plone.directives import dexterity, form

from zope import schema
from plone.indexer import indexer

from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText

from hph.publications import MessageFactory as _


class IPublication(form.Schema, IImageScaleTraversable):
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
    form.widget(thirdPartyProject=CheckBoxFieldWidget)
    thirdPartyProject = schema.Set(
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


@indexer(IPublication)
def authorLastNameIndexer(obj):
    return obj.lastname
grok.global_adapter(authorLastNameIndexer, name="lastname")


@indexer(IPublication)
def thirdPartyProjectIndexer(obj):
    return obj.thirdPartyProject
grok.global_adapter(thirdPartyProjectIndexer, name="thirdPartyProject")


@indexer(IPublication)
def pubMediumIndexer(obj):
    return obj.media
grok.global_adapter(pubMediumIndexer, name="media")


@indexer(IPublication)
def pubSeriesIndexer(obj):
    return obj.bookSeries
grok.global_adapter(pubSeriesIndexer, name="bookSeries")


class Publication(dexterity.Item):
    grok.implements(IPublication)


class View(grok.View):
    grok.context(IPublication)
    grok.require('zope2.View')
    grok.name('view')
