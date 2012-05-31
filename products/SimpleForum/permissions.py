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
$Id: permissions.py 5400 2006-05-17 08:06:00Z clebeaupin $
"""
__author__  = 'Jerome Sandarnaud'
__docformat__ = 'restructuredtext'


#from Products.CMFCore.CMFCorePermissions import setDefaultRoles

try:
    from Products.CMFCore.permissions import setDefaultRoles     # Future support : CMF 1.5 / Plone 2.1
except ImportError:
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles

# Add permissions differ for each type, and are imported by __init__.initialize
AddSimpleForumFolder = 'SimpleForum: Add Forum Folder'
AddSimpleForum = 'SimpleForum: Add Forum'
AddSimpleForumPost = 'SimpleForum: Add Post'
EditSimpleForumPost = 'SimpleForum: Edit Post'
#ApproveSimpleForumPost = 'SimpleForum: Approve Post'  # Not yet used, maybe later ! Also, depends on workflow.

# Set up default roles for permissions
setDefaultRoles(AddSimpleForumFolder, ('Manager', 'Owner',))
setDefaultRoles(AddSimpleForum, ('Manager', 'Owner',))
setDefaultRoles(AddSimpleForumPost, ('Manager', 'Owner',))
setDefaultRoles(EditSimpleForumPost, ('Manager', 'Owner',))
#setDefaultRoles(ApproveSimpleForumPost, ('Manager', 'Reviewer'))