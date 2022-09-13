# -*- coding: utf-8 -*-
"""Module providing custom catalog indexers"""
from hph.publications.publication import IPublication
from plone.indexer import indexer


@indexer(IPublication)
def index_author_last_name(obj):
    indexed_data = getattr(obj, 'lastname', False)
    return indexed_data


@indexer(IPublication)
def index_external_funds_project(obj):
    indexed_data = getattr(obj, 'externalFundsProject', False)
    return indexed_data


@indexer(IPublication)
def index_media(obj):
    indexed_data = getattr(obj, 'media', False)
    return indexed_data


@indexer(IPublication)
def index_book_series(obj):
    indexed_data = getattr(obj, 'bookSeries', False)
    return indexed_data
