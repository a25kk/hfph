from five import grok

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from hph.sitecontent import MessageFactory as _


class ThirdPartyProjectsVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        TYPES = {
            _(u"Rottendorf Project"): 'rottendorf',
            _(u"Philosophy and Motivation"): 'motivation',
            _(u"Philosophy and Leadership"): 'leadership',
            _(u"IGP"): 'igp',
            _(u"Mediaethics"): 'mediaethics',
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in TYPES.iteritems()])
grok.global_utility(ThirdPartyProjectsVocabulary,
                    name=u"hph.sitecontent.thirdPartyProjects")
