# -*- coding: utf-8 -*-
"""Module providing panel page vocabularies"""
from binascii import b2a_qp

from zope.interface import implementer
from zope.schema. interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

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
            'widget--tile': _(u'Tile'),
            'ui--calendar': _(u'Calendar'),
            'content--calendar-clock': _(u'Calendar with Clock'),
            'content--classroom': _(u'Classroom'),
            'content--counseling': _(u'Counseling'),
            'content--download-action': _(u'Download'),
            'content--research': _(u'Research'),
            'content--teacher': _(u'Teacher'),
        }
        return display_options


TeaserLinkIconVocabulary = TeaserLinkIconVocabularyFactory()
