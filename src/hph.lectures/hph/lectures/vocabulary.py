from five import grok

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from hph.lectures import MessageFactory as _


class CourseSemesterVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        TYPES = {
            _(u"Summer Semester"): 'summer-semester',
            _(u"Winter Semester"): 'winter-semester'
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in TYPES.iteritems()])
grok.global_utility(CourseSemesterVocabulary,
                    name=u"hph.lectures.CourseSemester")


class CourseDurationVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        TYPES = {
            _(u"1 hour"): '1-hour',
            _(u"2 hour"): '2-hour',
            _(u"3 hour"): '3-hour',
            _(u"4 hour"): '4-hour'
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in TYPES.iteritems()])
grok.global_utility(CourseDurationVocabulary,
                    name=u"hph.lectures.CourseDuration")


class CourseTypeVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        TYPES = {
            _(u"Lecture"): 'lecture',
            _(u"Introductory seminar source"): 'introductory-seminar-course',
            _(u"Advanced seminar"): 'advanced',
            _(u"Exercise"): 'exercise',
            _(u"Colloquium"): 'colloquium',
            _(u"Basic module"): 'basic',
            _(u"Reading course"): 'reading'
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in TYPES.iteritems()])
grok.global_utility(CourseTypeVocabulary, name=u"hph.lectures.CourseType")


class CourseDegreeVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        DEGREES = {
            _(u"BA"): 'ba',
            _(u"MA Ethics"): 'ma-ethics',
            _(u"MA kons"): 'ma-kons',
            _(u"BA"): 'ba',
            _(u"Mag"): 'magister',
            _(u"ZEP"): 'zep',
            _(u"MA-IB"): 'ma-ib'
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                for title, value
                                in DEGREES.iteritems()])
grok.global_utility(CourseDegreeVocabulary, name=u"hph.lectures.CourseDegree")
