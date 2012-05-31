## -*- coding: utf-8 -*-
## Copyright (C)2006 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
$Id: SimpleForumCatalog.py 5400 2006-05-17 08:06:00Z clebeaupin $
"""

__author__  = 'Jerome Sandarnaud'
__docformat__ = 'restructuredtext'

# Zope imports
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZCatalog.ZCatalog import ZCatalog

# Products imports
from Products.SimpleForum.config import CATALOG_ID

class SimpleForumCatalog(ZCatalog):
    """Catalog for PloneSimpleForum"""

    id = CATALOG_ID
    title = "Forum Catalog"
    
    security = ClassSecurityInfo()
    
    def __init__(self):
        ZCatalog.__init__(self, self.getId())
        
        # Build catalog
        self._initIndexes()

    def _initIndexes(self):
        """Init indexes and metadata of catalog"""
        
        for index_name, index_type in self.enumerateIndexes():
            try: #ugly try catch XXX FIXME
                if index_name not in self.indexes():
                    self.addIndex(index_name, index_type, extra=None)
                if not index_name in self.schema():
                    self.addColumn(index_name)
            except:
                pass
    
    security.declarePublic('enumerateIndexes')
    def enumerateIndexes(self):
        """Returns indexes used by catalog"""
        return (
                ('UID', 'FieldIndex'),
                ('id', 'FieldIndex'),
                ('Title', 'TextIndex'),
                ('getLevel', 'FieldIndex'),
                ('created', 'DateIndex'),
                ('modified', 'DateIndex'),
                ('getPostAuthor', 'FieldIndex'),
                ('path', 'PathIndex'),
                )
    
    def __url(self, object):
        """Returns url of object"""
        return '/'.join(object.getPhysicalPath())
    
    security.declarePrivate('indexObject')
    def indexObject(self, object):
        '''Add to catalog.'''
        url = self.__url(object)
        self.catalog_object(object, url)

    security.declarePrivate('unindexObject')
    def unindexObject(self, object):
        '''Remove from catalog.'''
        url = self.__url(object)
        self.uncatalog_object(url)

    security.declarePrivate('reindexObject')
    def reindexObject(self, object, idxs=[]):
        """Update catalog after object data has changed.
        The optional idxs argument is a list of specific indexes
        to update (all of them by default).
        """
        url = self.__url(object)
        if idxs != []:
            # Filter out invalid indexes.
            valid_indexes = self._catalog.indexes.keys()
            idxs = [i for i in idxs if i in valid_indexes]
        self.catalog_object(object, url, idxs=idxs)

InitializeClass(SimpleForumCatalog)

def manage_addSimpleForumCatalog(self, REQUEST=None):
    """Add the forum catalog"""
    c = SimpleForumCatalog()
    self._setObject(c.getId(), c)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST,update_menu=1)
