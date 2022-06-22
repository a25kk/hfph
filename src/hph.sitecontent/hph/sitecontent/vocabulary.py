from binascii import b2a_qp

# from five import grok
from zope.interface import implementer

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from hph.sitecontent import MessageFactory as _


@implementer(IVocabularyFactory)
class EventCategoryVocabularyFactory(object):
    def __call__(self, context):
        TYPES = {
            _("Studies"): "studies",
            _("Research"): "research",
            _("Public Event"): "public-event",
        }
        return SimpleVocabulary(
            [SimpleTerm(value, title=title) for title, value in TYPES.items()]
        )


EventCategoryVocabulary = EventCategoryVocabularyFactory()


@implementer(IVocabularyFactory)
class ThirdPartyProjectsVocabularyFactory(object):

    def __call__(self, context):
        TYPES = {
            _("Rottendorf Project"): "rottendorf",
            _("Philosophy and Motivation"): "motivation",
            _("Philosophy and Leadership"): "leadership",
            _("IGP"): "igp",
            _("Mediaethics"): "mediaethics",
        }
        return SimpleVocabulary(
            [SimpleTerm(value, title=title) for title, value in TYPES.items()]
        )


ThirdPartyProjectsVocabulary = ThirdPartyProjectsVocabularyFactory()
