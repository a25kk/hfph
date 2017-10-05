from five import grok

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer

from hph.lectures import MessageFactory as _


def degree_courses():
    courses = {
        _(u"BA (Bachelor)"): 'ba',
        _(u"MAcons (Consecutive Master)"): 'macon',
        _(u"MA-Ethics (Continuing Master Ethics)"): 'ma-ethic',
        _(u"MA-IE (Continuing Master Intercultural Education)"): 'ma-ib',
    }
    return courses


def degree_courses_tokens():
    courses = {
        'ba': _(u"BA"),
        'macon': _(u"MAcons"),
        'ma-ethic': _(u"MA-Ethics"),
        'ma-ib': _(u"MA-IE")
    }
    return courses


def learning_modules_master():
    modules = {
        'I': _(u"I"),
        'II': _(u"II"),
        'III': _(u"III"),
        'IV': _(u"IV"),
        'V': _(u"V"),
        'VI': _(u"VI"),
        'VII': _(u"VII")
    }
    return modules


def learning_modules_bachelor():
    """
    Vocabulary for learning module selection
    :return: dictionary of modules
    """
    modules = {
        'I/1':  _(u"I/1"),
        'I/2': _(u"I/2"),
        'I/3':  _(u"I/3"),
        'I/4':  _(u"I/4"),
        'I/5':  _(u"I/5"),
        'I/6':  _(u"I/6"),
        'II/1': _(u"II/1"),
        'II/2': _(u"II/2"),
        'II/3': _(u"II/3"),
        'II/4': _(u"II/4"),
        'II/5': _(u"II/5"),
        'II/6': _(u"II/6"),
        'III/1': _(u"III/1"),
        'III/2': _(u"III/2"),
        'IV/1': _(u"IV/1"),
        'IV/2': _(u"IV/2"),
        'wp-theology': _(u"WP Theology"),
        'wp-cultures': _(u"WP Cultures"),
        'wp-globalization': _(u"WP Globalization"),
        'wp-environmental-ethics': _(u"WP Environmental Ethics"),
        'wp-nature-philosophy': _(u"WP Nature Philosophy"),
        'wp-logic': _(u"WP Logic"),
        'wp-media': _(u"WP Media"),
        'wp-cultural-admission': _(u"WP Cultural Admission"),
        'wp-education': _(u"WP Education"),
        'wp-internship': _(u"WP Internship"),
    }
    return modules


def course_core_themes():
    """
    Core themes for each degree course
    :return: dictionary
    """
    themes = {
        'macon': {
            'gn': _('GN'),
            'rv': _('RV'),
            'eg': _('EG')
        },
        'ma-ethic': {
            'wir': _('WIR'),
            'med': _('MED'),
            'mez': _('MEZ')
        },
        'ma-ib': {
            'ie': _('IE'),
            'vv': _('VV'),
            'sc': _('SC'),
            'pb': _('PB')
        }
    }
    return themes


def course_core_theme_names():
    """
    Core themes for each degree course
    :return: dictionary
    """
    themes = {
        'gn': _('Spirit and Nature (GN)'),
        'rv': _('Religion and Reason (RV)'),
        'eg': _('Ethics and Society (EG)'),
        'wir': _('Business Ethics (WIR)'),
        'med': _('Media Ethics (MED)'),
        'mez': _('Medicine Ethics (MEZ)'),
        'ie': _('Intercultural Education (IE)'),
        'vv': _('International Understanding (VV)'),
        'sc': _('Spiritual Care (SC)'),
        'pb': _('Personal Development (PB)')
    }
    return themes


def module_studies_vocabulary(context):
    """Vocabulary with all available module studies recommendations.
    """
    module_studies_recommendations = {
        _(u"Philosophicum"): 'philosophicum',
        _(u"Module Studies Economic Ethics"): 'economic-ethics',
        _(u"Module Studies Adult Education"): 'adult-education',
        _(u"Module Studies Personal Development"): 'personal-development',
        _(u"Philosophy & Leadership Certificate"):
            'philosophy-leadership-certificate',
        _(u"Module Studies Media Ethics"): 'media-ethics',
        _(u"Module Studies International Understanding"):
            'international-understanding',
        _(u"Global Solidarity"): 'global-solidarity',
        _(u"Module Studies Medicine Ethics"): 'medicine-ethics',
        _(u"Module Studies Spiritual Care"): 'spiritual-care',
    }
    terms = [
        SimpleTerm(value, title=title)
        for title, value in module_studies_recommendations.iteritems()
    ]
    return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class ModuleStudiesVocabularyFactory(object):
    """ Recommended module studies for a lecture """
    def __call__(self, context):
        module_studies = {
            _(u"Philosophicum"): 'philosophicum',
            _(u"Economic Ethics"): 'economic-ethics'
        }
        terms = [
            SimpleTerm(value, title=title)
            for title, value in module_studies.iteritems()
        ]
        return SimpleVocabulary(terms)


class ModuleStudiesVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        module_studies = {
            _(u"Philosophicum"): 'philosophicum',
            _(u"Economic Ethics"): 'economic-ethics'
        }
        return SimpleVocabulary([SimpleTerm(value, title=title)
                                 for title, value
                                 in module_studies.iteritems()])
grok.global_utility(ModuleStudiesVocabulary,
                    name=u"hph.lectures.moduleStudies")


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
