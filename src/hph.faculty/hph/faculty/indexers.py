# -*- coding: utf-8 -*-
"""Module providing custom catalog indexers"""
from hph.faculty.facultymember import IFacultyMember
from plone.indexer import indexer


@indexer(IFacultyMember)
def index_ast_name(obj):
    indexed_data = getattr(obj, 'lastname', False)
    return indexed_data


@indexer(IFacultyMember)
def index_academic_role(obj):
    indexed_data = getattr(obj, 'academicRole', False)
    return indexed_data
