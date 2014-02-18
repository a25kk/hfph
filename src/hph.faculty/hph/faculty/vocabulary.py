from five import grok

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from hph.faculty import MessageFactory as _


class FacultyMemberPositionVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        TYPES = {
            _(u"Lecturer"): 'lecturer',
            _(u"Professor"): 'professor',
            _(u"docent"): 'docent',
            _(u"Emeriti"): 'emeriti'
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in TYPES.iteritems()])
grok.global_utility(FacultyMemberPositionVocabulary,
                    name=u"hph.faculty.facultyMemberPosition")
