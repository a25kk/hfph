from five import grok
from plone.directives import dexterity, form

from zope import schema
from plone.indexer import indexer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText

from hph.publications import MessageFactory as _

media = SimpleVocabulary(
    [SimpleTerm(value=u'book', title=_(u'Book')),
     SimpleTerm(value=u'magazine', title=_(u'Magazine')),
     SimpleTerm(value=u'digital', title=_(u'DVD/CD'))])

series = SimpleVocabulary(
    [SimpleTerm(value=u'global-culture', title=_(u'Global Culture')),
     SimpleTerm(value=u'solidarity', title=_(u'Solidarity')),
     SimpleTerm(value=u'philosophy', title=_(u'Philosophy')),
     SimpleTerm(value=u'contexts', title=_(u'Contexts')),
     SimpleTerm(value=u'munich', title=_(u'Munich Philosophy')),
     SimpleTerm(value=u'theology', title=_(u'Theology')),
     ])

display = SimpleVocabulary(
    [SimpleTerm(value=u'rottendorf', title=_(u'Rottendorf Project')),
     SimpleTerm(value=u'motivation', title=_(u'Philosophy and Motivation')),
     SimpleTerm(value=u'leadership', title=_(u'Philosophy and Leadership')),
     SimpleTerm(value=u'igp', title=_(u'IGP'))])


class IPublication(form.Schema, IImageScaleTraversable):
    """
    A single publication like a book, dvd or magazine
    """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    publication = schema.TextLine(
        title=_(u"Year of Publication"),
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
    form.widget(medium=CheckBoxFieldWidget)
    medium = schema.Set(
        title=_(u"Medium"),
        value_type=schema.Choice(
            title=_(u"Media Selection"),
            vocabulary=media,
        ),
        required=True,
    )
    form.widget(series=CheckBoxFieldWidget)
    series = schema.Set(
        title=_(u"Series"),
        value_type=schema.Choice(
            title=_(u"Series Selection"),
            vocabulary=series,
        ),
        required=True,
    )
    form.widget(thirdPartyProject=CheckBoxFieldWidget)
    thirdPartyProject = schema.Set(
        title=_(u"Third Party Project Display"),
        value_type=schema.Choice(
            title=_(u"Display Selection"),
            vocabulary=u'hph.sitecontent.thirdPartyProjects',
        ),
        required=True,
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
    return obj.authorLastName
grok.global_adapter(authorLastNameIndexer, name="autorLastName")


@indexer(IPublication)
def thirdPartyProjectIndexer(obj):
    return obj.thirdPartyProject
grok.global_adapter(thirdPartyProjectIndexer, name="thirdPartyProject")


@indexer(IPublication)
def pubMediumIndexer(obj):
    return obj.medium
grok.global_adapter(pubMediumIndexer, name="medium")


@indexer(IPublication)
def pubSeriesIndexer(obj):
    return obj.series
grok.global_adapter(pubSeriesIndexer, name="series")


class Publication(dexterity.Item):
    grok.implements(IPublication)


class View(grok.View):
    grok.context(IPublication)
    grok.require('zope2.View')
    grok.name('view')
