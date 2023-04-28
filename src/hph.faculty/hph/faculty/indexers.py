# -*- coding: utf-8 -*-
"""Module providing custom catalog indexers"""
from plone.indexer import indexer

from hph.faculty.facultymember import IFacultyMember


@indexer(IFacultyMember)
def index_ast_name(obj):
    indexed_data = getattr(obj, 'lastname', False)
    return indexed_data


@indexer(IFacultyMember)
def index_academic_role(obj):
    indexed_data = getattr(obj, 'academicRole', False)
    return indexed_data
