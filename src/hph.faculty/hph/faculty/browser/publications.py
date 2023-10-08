# -*- coding: utf-8 -*-
"""Module providing publication listing"""
from operator import attrgetter

from zope.schema.vocabulary import getVocabularyRegistry

from plone import api

from Acquisition import aq_inner, aq_parent
from Products.Five import BrowserView


class FacultyMemberPublicationsView(BrowserView):
    """ List associated publications for faculty member"""

    def __call__(self):
        return self.render()

    @property
    def has_publications(self):
        if self.associated_publications():
            return True
        return False

    def render(self):
        return self.index()

    def parent_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def computed_klass(self, value):
        context = aq_inner(self.context)
        active_filter = getattr(context, 'academicRole', None)
        klass = 'c-nav-list__item'
        if active_filter == value:
            klass += ' c-nav-list__item--active'
        return klass

    def associated_publications(self):
        context = aq_inner(self.context)
        assigned = getattr(context, 'associatedPublications', None)
        return assigned

    @staticmethod
    def get_publication_details(uuid):
        item = api.content.get(UID=uuid)
        return item

    def publications(self):
        publications = [self.get_publication_details(item)
                        for item in self.associated_publications()]
        sorted_publications = sorted(
            publications,
            key=attrgetter('publicationYear'),
            reverse=True
        )
        return sorted_publications
