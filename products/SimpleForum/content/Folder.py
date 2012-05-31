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
$Id: Folder.py 5415 2006-08-30 09:58:06Z clebeaupin $
"""
__author__  = 'Jerome Sandarnaud'
__docformat__ = 'restructuredtext'

# Zope imports
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

# CMF imports
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils  import getToolByName

# Archetypes imports
from Products.Archetypes.public import *

# Products imports
from Products.SimpleForum.interfaces import ISimpleForumFolder, ISimpleForum
from Products.SimpleForum.config import PROJECTNAME, I18N_DOMAIN

# SimpleForumFolder schema
SimpleForumFolderSchema = OrderedBaseFolderSchema.copy()

class SimpleForumFolder(OrderedBaseFolder):
    """Folder aggregating all forums"""
    
    portal_type = meta_type = 'SimpleForumFolder'
    archetype_name = 'Forum Folder'
    immediate_view = 'simpleforumfolder_view'
    default_view   = 'simpleforumfolder_view'
    global_allow = True
    filter_content_types = True
    allowed_content_types = ('SimpleForum',)
    content_icon = 'folder_icon.gif'
    __implements__ = (OrderedBaseFolder.__implements__, ISimpleForumFolder,)
    _at_rename_after_creation = True # rename object according to the title?
        
    schema =  SimpleForumFolderSchema
    security = ClassSecurityInfo()
    
    actions = (
        {
        'id'            : 'view',
        'name'          : 'View',
        'action'        : 'string:${object_url}/simpleforumfolder_view',
        'permissions'   : (CMFCorePermissions.View, ),
        'category'      : 'object',
        'visible'       : 1,
        },
        {
        'id'          : 'local_roles',
        'name'        : 'Sharing',
        'action'      : 'string:${object_url}/folder_localrole_form',
        'permissions' : (CMFCorePermissions.ManageProperties,),
         },)
    
    security.declareProtected(CMFCorePermissions.View, 'getForumFolder')
    def getForumFolder(self):
        """Returns the object itself. Very useful to find a forum folder by 
        acquisition"""
        
        return self
    
    security.declareProtected(CMFCorePermissions.View, 'getForums')
    def getForums(self):
        """Returns all forum objects this folder contained"""
        
        return [x for x in self.objectValues() if ISimpleForum.isImplementedBy(x)]
    
    security.declareProtected(CMFCorePermissions.View, 'getForumItems')
    def getForumItems(self):
        """Returns a list of forum items (simple dictionnary).
        This list is sorted on forum position in this folder
        
        Structure of each item:
        - title: title of forum
        - description: Description of forum
        - url: url of forum
        - path: path of forum
        - topics_count: number of topics in this forum
        - posts_count: number of posts in this forum
        - last_topic_title: title of last topic added in this forum
        - last_topic_url: url of last topic added in this forum
        - last_topic_created: Creation date of last topic added in this forum
        - last_post_title: title of last post added in this forum
        - last_post_url: url of last post added in this forum
        - last_post_created: Creation date of last post added in this forum
        """
        forum_items = []
        
        # Get all forums
        forums = self.getForums()
        
        # Loop on forums and query all forum catalogs
        for forum in forums:
            # Build item
            item = {}
            item['title'] = forum.title_or_id()
            item['description'] = forum.Description()
            item['url'] = forum.absolute_url()
            item['path'] = '/'.join(forum.getPhysicalPath())
            
            # Get all post brains to get these informations:
            # - topics_count
            # - posts_cout
            # - last_topic_title
            # - last_topic_url
            # - last_post_title
            # - last_post_url
            brains = forum.getPostBrains(sort_on='created')
            item['posts_count'] = len(brains)
            item['topics_count'] = len(forum) - 1 # Remove catalog in the count
            item['last_topic_title'] = ''
            item['last_topic_url'] = ''
            item['last_topic_created'] = None
            item['last_post_title'] = ''
            item['last_post_url'] = ''
            item['last_post_created'] = None
            
            # Search last topic and last post
            if brains:
                post_brain = brains[-1]
                post_obj = post_brain.getObject()
                topic_obj = post_obj.getTopic()
                item['last_topic_title'] = topic_obj.title_or_id()
                item['last_topic_url'] = topic_obj.absolute_url()
                item['last_topic_created'] = topic_obj.created()
                item['last_post_title'] = post_obj.title_or_id()
                item['last_post_url'] = post_obj.absolute_url()
                item['last_post_created'] = post_obj.created()
            
            forum_items.append(item)
        return forum_items
    
registerType(SimpleForumFolder, PROJECTNAME)
