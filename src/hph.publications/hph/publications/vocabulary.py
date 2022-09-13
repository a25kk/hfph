# from five import grok

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer

from hph.publications import MessageFactory as _


@implementer(IVocabularyFactory)
class PublicationMediaVocabulary(object):

    def __call__(self, context):
        MEDIA = {
            _(u"Book"): 'book',
            _(u"Magazine"): 'magazine',
            _(u"DVD/CD"): 'digital',
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in MEDIA.iteritems()])


PublicationMediaVocabulary = PublicationMediaVocabulary()


@implementer(IVocabularyFactory)
class PublicationSeriesVocabulary(object):

    def __call__(self, context):
        TYPES = {
            _(u"Global Culture"): 'global-culture',
            _(u"Solidarity"): 'solidarity',
            _(u"Philosophy"): 'philosophy',
            _(u"Contexts"): 'contexts',
            _(u"Munich Philosophy"): 'munich',
            _(u"Practical Philosophy"): 'practical-philosophy',
            _(u"Boundary Studies"): 'boundary-studies'
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in TYPES.iteritems()])


PublicationSeriesVocabulary = PublicationSeriesVocabulary()
