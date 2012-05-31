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
$Id: Forum.py 5420 2006-09-22 11:38:38Z clebeaupin $
"""
__author__  = 'Jerome Sandarnaud'
__docformat__ = 'restructuredtext'

# Python imports
from random import random

# Zope imports
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from DateTime import DateTime

# CMF imports
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils  import getToolByName

# Archetypes imports
from Products.Archetypes.public import *

# Products imports
from Products.SimpleForum.interfaces import ISimpleForum
from Products.SimpleForum.config import PROJECTNAME, I18N_DOMAIN, CATALOG_ID
from Products.SimpleForum.SimpleForumCatalog import manage_addSimpleForumCatalog
from Products.SimpleForum.permissions import AddSimpleForumPost

# SimpleForum schema
SimpleForumSchema = BaseBTreeFolderSchema.copy()
SimpleForumSchema['description'].isMetadata = False
SimpleForumSchema['description'].schemata = 'default'


class PostFactoryMixin:
    """Provides method to create post object"""
    security = ClassSecurityInfo()
    post_type_name = 'SimpleForumPost'
    
    security.declarePrivate('_generatePostId')
    def _generatePostId(self):
        """Returns an id for a post"""
        
        now = DateTime()
        post_time = '%s%s' % (now.strftime('%Y%m%d'), str(now.millis())[7:])
        post_random = str(random())[2:6]
        return 'post%s%s' %(post_time, post_random)
    
    security.declareProtected(AddSimpleForumPost, 'createPost')
    def createPost(self, quote=False):
        """Shortcut to create new post in a forum
        
        @param quote: If true quote parent post"""
        
        post_id = self._generatePostId()
        post_type = self.post_type_name
        ftool = getToolByName(self, 'portal_factory')
        if ftool.getFactoryTypes().has_key(post_type):
            obj = self.restrictedTraverse('portal_factory/' + post_type + '/' + post_id)
        else:
            self.invokeFactory(type_name=post_type, id=post_id)
            obj = getattr(self, post_id)
            
        return obj.base_edit()
            
InitializeClass(PostFactoryMixin)  

class SimpleForum(BaseBTreeFolder, PostFactoryMixin):
    """PloneSimpleForum container"""
    
    portal_type = meta_type = 'SimpleForum'
    archetype_name = 'Forum'
    immediate_view = 'simpleforum_view'
    default_view   = 'simpleforum_view'
    global_allow = True
    filter_content_types = True
    allowed_content_types = ('SimpleForumPost',)
    content_icon = 'simpleforum_icon.gif'
    __implements__ = (BaseBTreeFolder.__implements__, ISimpleForum,)
    _at_rename_after_creation = True # rename object according to the title?
        
    schema = SimpleForumSchema
    security = ClassSecurityInfo()

    actions = (
        {
        'id'            : 'view',
        'name'          : 'View',
        'action'        : 'string:${object_url}/simpleforum_view',
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
    
    security.declareProtected(CMFCorePermissions.View, 'getForum')
    def getForum(self):
        """Returns the object itself. Very useful to find a forum by 
        acquisition"""
        
        return self
    
    security.declareProtected(CMFCorePermissions.View, 'getPostBrains')
    def getPostBrains(self, **kwargs):
        """Call forum catalog searchResults method and returns all post brains
        
        @param kwargs: Extra arguments used in the searchResults method"""
        
        cat = self.getCatalog()
        query = {}
        query.update(kwargs)
        return cat(**kwargs)
        
    security.declareProtected(CMFCorePermissions.View, 'getPosts')
    def getPosts(self, **kwargs):
        """Returns all posts contained in this forum
        
        @param kwargs: Extra arguments to find posts"""
        
        return [x.getObject() for x in self.getPostBrains(**kwargs)]
        
    security.declareProtected(CMFCorePermissions.View, 'getTopicBrains')
    def getTopicBrains(self, **kwargs):
        """Returns the topic object. Very useful to find a topic by 
        acquisition.
        A topic is the root post of a discussion.
        Posts having length equals to 1 are topic
        
        @param kwargs: Extra arguments to find topics
        """
        
        query = {}
        query.update(kwargs)
        query['getLevel'] = 1
        return self.getPostBrains(**query)
    
    security.declareProtected(CMFCorePermissions.View, 'getTopics')
    def getTopics(self, **kwargs):
        """Returns all topics contained in this forum
        
        @param kwargs: Extra arguments to find posts"""
        
        return [x.getObject() for x in self.getTopicBrains(**kwargs)]
        
    security.declareProtected(CMFCorePermissions.View, 'getTopicItems')
    def getTopicItems(self, sort_on='topic'):
        """Returns a list of topic items (simple dictionnary).
        This list can sorted on :
            - topic creation date in reverse.
            - post creation date in reverse.
        
        Structure of each item:
        - title: title of topic 
        - url: url of topic
        - path: path of topic
        - author: author of topic
        - anonymous: is the author of topic anonymous ?
        - created: creation date
        - posts_count : number of replies in this topic
        - last_post_created: Creation date of last post added in this forum
        
        @param sort_on: (topic or post)
        """
        
        # Get all post brains
        brains = self.getPostBrains(sort_on='getLevel')
        path_to_topic = {}

        # Loop on brains
        for brain in brains:
            level = brain['getLevel']
            path = brain.getPath()
            
            if level == 1:
                # This is a topic
                item = {}
                item['title'] = brain['Title'] or brain['id']
                item['url'] = brain.getURL()
                item['path'] = path
                item['author'] = brain['getPostAuthor']
                item['anonymous'] = (item['author'] == 'Anonymous User')
                item['created'] = brain['created']
                item['posts_count'] = 0
                item['last_post_created'] = brain['created']
                path_to_topic[path] = item
            else:
                # This is a reply of topic
                topic_path = '/'.join(path.split('/')[:(-level+1)])
                path_to_topic[topic_path]['posts_count'] += 1
                
                # Get oldeset post of topic and store its date
                created = brain['created']
                if created and \
                   created > path_to_topic[topic_path]['last_post_created']:
                    path_to_topic[topic_path]['last_post_created'] = created
        
        # Get topic items and sort them on creation date
        sort_index = 'created'
        
        if sort_on == 'post':
            sort_index = 'last_post_created'
        
        def sort_date(one, two):
           return cmp(two[sort_index], one[sort_index])
           
        topic_items = path_to_topic.values()
        topic_items.sort(sort_date)
        
        return topic_items
    
    ######################
    # Catalog support
    ######################
  
    def _initCatalog(self):
        """Add forum catalog"""
        
        if not hasattr(self, CATALOG_ID):
            add_catalog = manage_addSimpleForumCatalog
            add_catalog(self)
        
        catalog = getattr(self, CATALOG_ID)
        catalog.manage_reindexIndex()
        return catalog
    
    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        BaseBTreeFolder.manage_afterAdd(self, item, container)
        # Add catalog
        self._initCatalog()

    security.declareProtected('View', 'getCatalog')
    def getCatalog(self):
        """Returns catalog of Forum"""
        
        if not hasattr(self, CATALOG_ID):
            # Build catalog if it doesn't exist
            catalog = self._initCatalog()
        
        catalog = getattr(self, CATALOG_ID)
        utool = getToolByName(self, 'portal_url')
        return self.restrictedTraverse(utool.getRelativeContentURL(catalog))    
    
    
registerType(SimpleForum, PROJECTNAME)
