# -*- coding: utf-8 -*-
"""Module providing panel page vocabularies"""
from binascii import b2a_qp

from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from ade25.panelpage import MessageFactory as _


@implementer(IVocabularyFactory)
class TeaserLinkIconVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_display_options()
        terms = [
            self.generate_simple_term(widget_key, widget_term)
            for widget_key, widget_term in widgets.items()
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def generate_simple_term(widget, widget_term):
        term = SimpleTerm(
            value=widget,
            token=b2a_qp(widget.encode('utf-8')),
            title=_(widget_term)
        )
        return term

    @staticmethod
    def get_display_options():
        display_options = {
            'content--lecture-directory': _(u'Lecture Directory'),
            'content--semester-dates': _(u'Semester Dates'),
            'content--course-guidance-service': _(u'Course Guidance Service'),
            'content--study-downloads': _(u'Study Downloads'),
            'content--education': _(u'Education'),
            'content--further-education': _(u'Further Education'),
            'content--research-projects': _(u'Research projects'),
            'content--teachers': _(u'Teachers'),
        }
        return display_options


TeaserLinkIconVocabulary = TeaserLinkIconVocabularyFactory()
