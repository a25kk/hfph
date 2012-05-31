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
$Id: __init__.py 5407 2006-05-18 08:15:46Z roeder $
"""
__author__  = 'Jerome Sandarnaud'
__docformat__ = 'restructuredtext'

# Python imports
import sys
from Globals import package_home

# CMF imports
from Products.CMFCore import utils
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.DirectoryView import registerDirectory

# Archetypes imports
from Products.Archetypes.public import process_types, listTypes

# Products imports
from Products.SimpleForum.config import PROJECTNAME, GLOBALS, SKINS_DIR
from Products.SimpleForum.content import *
from Products.SimpleForum.tool import SimpleForumTool
#from Products.SimpleForum.interfaces import ISimpleForum

# Apply FactoryTool patch to allow Anonymous posts on Plone 2.0.5
#import patches

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    listOfTypes = listTypes(PROJECTNAME)
    content_types, constructors, ftis = process_types(listOfTypes, PROJECTNAME)
    
    # Assign an own permission to all content types
    # Heavily based on Bricolite's code from Ben Saller
    import permissions as perms

    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: %s" % (PROJECTNAME, atype.archetype_name)
        utils.ContentInit(
            kind,
            content_types      = (atype,),
            # Note : Add permissions look like perms.Add{meta_type}
            permission         = getattr(perms, 'Add%s' % atype.meta_type),
            extra_constructors = (constructor,),
            fti                = ftis,
            ).initialize(context)
            
    # Import tool
    utils.ToolInit(
        '%s Tool' % PROJECTNAME,
        tools=(SimpleForumTool,),
        icon='tool.gif').initialize(context)

