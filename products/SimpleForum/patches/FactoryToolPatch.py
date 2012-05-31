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
Patch for Plone factory tool _getTempFolder method

Copied from CMFPlacefullWorkflow where it was originally
provided by E.D. (Ingeniweb)
"""
__version__ = "$Revision: 1.4 $"
# $Source: /cvsroot/ingeniweb/SimpleForum/patches/FactoryToolPatch.py,v $
# $Id: FactoryToolPatch.py,v 1.4 2006/05/17 08:04:44 clebeaupin Exp $
__docformat__ = 'restructuredtext'

# Zope imports
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_parent, aq_inner
from AccessControl.Permission import Permission

# Plone imports
from Products.CMFPlone.FactoryTool import FactoryTool, FACTORY_INFO, TempFolder, ListType

def _getTempFolder(self, type_name):
    """
    monkey-patched by CMFPlacefulWorkflow to backport fix from Plone 2.1 to 2.0
    """
    AP = CMFCorePermissions.AddPortalContent
    
    factory_info = self.REQUEST.get(FACTORY_INFO, {})
    tempFolder = factory_info.get(type_name, None)
    if tempFolder:
        tempFolder = aq_inner(tempFolder).__of__(self)
        return tempFolder
    
    # make sure we can add an object of this type to the temp folder
    types_tool = getToolByName(self, 'portal_types')
    if not type_name in types_tool.TempFolder.allowed_content_types:
        # update allowed types for tempfolder
        types_tool.TempFolder.allowed_content_types = (types_tool.listContentTypes())
        
    tempFolder = TempFolder(type_name).__of__(self)
    intended_parent = aq_parent(self)
    portal = getToolByName(self, 'portal_url').getPortalObject()
    folder_roles = {} # mapping from permission name to list or tuple of roles
                      # list if perm is acquired; tuple if not
    n_acquired = 0    # number of permissions that are acquired

    # build initial folder_roles dictionary
    for p in intended_parent.ac_inherited_permissions(1):
        name, value = p[:2]
        p = Permission(name, value, intended_parent)
        roles = p.getRoles()
        folder_roles[name] = roles
        if type(roles) is ListType:
            n_acquired += 1

    # If intended_parent is not the portal, walk up the acquisition hierarchy and
    # acquire permissions explicitly so we can assign the acquired version to the
    # temp_folder.  In addition to being cumbersome, this is undoubtedly very slow.
    if intended_parent != portal:
        parent = aq_parent(aq_inner(intended_parent))
        while(n_acquired and parent != portal):
            n_acquired = 0
            for p in parent.ac_inherited_permissions(1):
                name, value = p[:2]
                roles = folder_roles[name]
                if type(roles) is ListType:
                    p = Permission(name, value, parent)
                    aq_roles = p.getRoles()
                    for r in aq_roles:
                        if not r in roles:
                            roles.append(r)
                    if type(aq_roles) is ListType:
                        n_acquired += 1
                    else:
                        roles = tuple(roles)
                    folder_roles[name] = roles
            parent = aq_parent(aq_inner(parent))
    for name, roles in folder_roles.items():
        tempFolder.manage_permission(name, roles, acquire=type(roles) is ListType)

    factory_info[type_name] = tempFolder
    self.REQUEST.set(FACTORY_INFO, factory_info)
    return tempFolder

# XXX We patch only Plone < 2.1: a better test should be found
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    FactoryTool._getTempFolder = _getTempFolder
