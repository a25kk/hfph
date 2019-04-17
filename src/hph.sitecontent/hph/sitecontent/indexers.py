# -*- coding: utf-8 -*-
"""Module providing custom catalog indexers"""
from Products.CMFCore.interfaces import IContentish
from plone.indexer import indexer


@indexer(IContentish)
def index_exclude_from_toc(obj):
    indexed_data = getattr(obj, 'exclude_from_toc', False)
    return indexed_data
