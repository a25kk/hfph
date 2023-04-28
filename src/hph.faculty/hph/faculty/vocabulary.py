from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from hph.faculty import MessageFactory as _


@implementer(IVocabularyFactory)
class AcademicRoleVocabularyFactory(object):

    def __call__(self, context):
        TYPES = {
            _(u"Professor"): 'professor',
            _(u"Lecturer"): 'lecturer',
            _(u"Emeriti"): 'emeriti'
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in TYPES.items()])


AcademicRoleVocabulary = AcademicRoleVocabularyFactory()
