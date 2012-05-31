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
This module contains the tool of SimpleForum product
"""

__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
import os
from StringIO import StringIO

# Zope imports
from Globals import package_home
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

# CMF imports
from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.ActionProviderBase import ActionProviderBase
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions

# Products imports
from Products.SimpleForum.config import PROJECTNAME, TOOL_ID, CATALOG_ID
from Products.SimpleForum.SimpleForumCatalog import manage_addSimpleForumCatalog

_www = os.path.join(os.path.dirname(__file__), 'www')

class SimpleForumTool(PropertyManager, UniqueObject, SimpleItem):
    """Provides utilities for SimpleForum"""

    plone_tool = 1
    id = TOOL_ID
    title = 'SimpleForum Tool'
    meta_type = 'SimpleForumTool'
    
    _properties=(
        {'id':'title', 'type': 'string', 'mode':'w'},
        )
        
    _actions = ()
            
    manage_options = (PropertyManager.manage_options +\
                    SimpleItem.manage_options +\
                    ({ 'label' : 'Migrate',
                      'action' : 'manage_migration'},)
                    )

    security = ClassSecurityInfo()
    
    security.declareProtected(CMFCorePermissions.ManagePortal, 'manage_migration')
    manage_migration = PageTemplateFile('manage_migration', _www)
    
    security.declareProtected(CMFCorePermissions.ManagePortal, 'manage_migrate')
    def manage_migrate(self, REQUEST=None):
        """Migrate all SimpleForum objects to the last installed version"""
        
        request = self.REQUEST
        logs = StringIO()
        dry_run = request.get('dry_run', False)
        
        # Search for all SimpleForum objects
        forum_meta_type = request.get('forum_meta_type', '')
        post_meta_type = request.get('post_meta_type', '')
        ctool = getToolByName(self, 'portal_catalog')
        forum_brains = ctool(meta_type=forum_meta_type)
        
        # Loop on SimpleForum objects and update catalog
        for forum_brain in forum_brains:
            forum_obj = forum_brain.getObject()
            
            # Remove old catalog
            forum_catalog = getattr(forum_obj, CATALOG_ID, None)
            if forum_catalog is not None:
                logs.write("Delete catalog: %s.<br />" % '/'.join(forum_catalog.getPhysicalPath()))
                if not dry_run:
                    forum_obj.manage_delObjects(ids=[CATALOG_ID])
            
            # Create new catalog
            if not dry_run:
                add_catalog = manage_addSimpleForumCatalog
                add_catalog(forum_obj)
                forum_catalog = getattr(forum_obj, CATALOG_ID, None)
            logs.write("Create new catalog: %s.<br />" % '/'.join(forum_catalog.getPhysicalPath()))
            
            # Search for all posts in forum and reindex all
            post_brains = ctool(path='/'.join(forum_obj.getPhysicalPath()), meta_type=post_meta_type)
            for post_brain in post_brains:
                post_obj = post_brain.getObject()
                if not dry_run:
                    forum_catalog.indexObject(post_obj)
                logs.write("Catalog reindex object: %s.<br />" % '/'.join(post_obj.getPhysicalPath()))

        if request is not None:
            message = "Migration completed."
            return self.manage_migration(self, manage_tabs_message = message, logs=logs.getvalue())

    security.declarePublic('getObjectFromPath')
    def getObjectFromPath(self, path):
        """Returns the object stored in path
        
        @param path: path of the object from portal
        """
        
        obj = None
        utool = getToolByName(self, 'portal_url')
        portal = utool.getPortalObject()
        
        try:
            obj = portal.restrictedTraverse(path)
        except:
            obj = None # path doesn't exist
        
        return obj

InitializeClass(SimpleForumTool)