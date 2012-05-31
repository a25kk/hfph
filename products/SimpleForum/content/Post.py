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
$Id: Post.py 5418 2006-09-14 08:22:17Z macadames $
"""
__author__  = 'Jerome Sandarnaud'
__docformat__ = 'restructuredtext'

# Python imports
from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent, aq_inner
import string

# CMF imports
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore  import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.public import *

# ATCT import
from Products.ATContentTypes.configuration import zconf

# Products imports
from Products.SimpleForum.interfaces import ISimpleForumPost
from Products.SimpleForum.config import PROJECTNAME, I18N_DOMAIN
from Products.SimpleForum.permissions import AddSimpleForumPost, \
    EditSimpleForumPost
from Products.SimpleForum.content.Forum import PostFactoryMixin

# SimpleForumPost schema
SimpleForumPostSchema = BaseFolderSchema.copy() + Schema((
    StringField(
        'postAuthor',
        #required=True,
        default_method='_getDefaultPostAuthor',
        write_permission=EditSimpleForumPost,
        widget=StringWidget(
            label='Post Author',
            label_msgid='label_post_author',
            i18n_domain=I18N_DOMAIN,
            ),
    ),
    TextField(
        'text',
        #required=True,
        searchable=True,
        primary=True,
        default_method='_getDefaultText',
        #validators=('isTidyHtmlWithCleanup',),
        default_content_type = zconf.ATDocument.default_content_type,
        default_output_type = 'text/x-html-safe',
        allowable_content_types = zconf.ATDocument.allowed_content_types,
        write_permission=EditSimpleForumPost,
        widget=RichWidget(
            label="Post Text",
            label_msgid="label_post_text",
            rows=15,
            i18n_domain=I18N_DOMAIN,
            ),
    ),
), marshall=RFC822Marshaller()
)

# We also need to set our own write permission for 'id' & 'title'
# This is usefull when we want Anonymous posts
SimpleForumPostSchema['id'].write_permission = EditSimpleForumPost
SimpleForumPostSchema['title'].write_permission = EditSimpleForumPost
SimpleForumPostSchema['title'].default_method = '_getDefaultTitle'

# Other schema fields tweaking
SimpleForumPostSchema['text'].widget.allow_file_upload = 0
SimpleForumPostSchema['text'].widget.allow_format_edit = 0

SimpleForumPostSchema['id'].widget.visible = {'view': 'invisible',
                                              'edit': 'invisible'}
SimpleForumPostSchema['postAuthor'].widget.visible = {'view': 'invisible',
                                                       'edit': 'invisible'}

# We also need to set our own permission for 'title' & 'description' ?
# This is usefull when you want Anonymous posts ?


class SimpleForumPost(BaseFolder, PostFactoryMixin):
    """PloneSimplePost """
    
    portal_type = meta_type = 'SimpleForumPost'
    archetype_name = 'Post'
    content_icon = 'simpleforumpost_icon.gif'
    immediate_view = 'simpleforumpost_view'
    default_view   = 'simpleforumpost_view'
    global_allow = False
    filter_content_types = True
    allowed_content_types = ('SimpleForumPost',)
    content_icon = 'simpleforumpost_icon.gif'
    __implements__ = (BaseFolder.__implements__, ISimpleForumPost,)
    #_at_rename_after_creation = False # rename object according to the title?
    
    schema =  SimpleForumPostSchema
    security = ClassSecurityInfo()

    actions = (
        {
        'id'            : 'view',
        'name'          : 'View',
        'action'        : 'string:${object_url}/simpleforumpost_view',
        'permissions'   : (CMFCorePermissions.View, ),
        'category'      : 'object',
        'visible'       : 1,
        },)
      
    security.declareProtected(CMFCorePermissions.View, 'getLevel')
    def getLevel(self):
        """
        Returns the depth from the forum object containing the post.
        Topic post has a level equals to 1
        """
        
        forum = self.getForum()
        obj_path = self.getPhysicalPath()
        depth = len(obj_path) - len(forum.getPhysicalPath())
        if 'portal_factory' in obj_path:
            depth -= 2
        return depth
    
    security.declareProtected(CMFCorePermissions.View, 'getPost')
    def getPost(self):
        """
        Returns the object itself
        """
        
        return self
    
    security.declareProtected(CMFCorePermissions.View, 'getReplies')
    def getReplies(self):
        """Returns all reply in a post."""
        
        return [x for x in self.objectValues() if ISimpleForumPost.isImplementedBy(x)]
        
    security.declareProtected(CMFCorePermissions.View, 'getParentPost')
    def getParentPost(self):
        """
        Returns the parent post object.
        Return None if the post is the topic
        """
        
        level = self.getLevel()
        if level == 1:
            # This is a topic so parent id a forum not a post
            return None
        
        # Get parent pots object
        forum = self.getForum()
        forum_path = forum.getPhysicalPath()
        obj_path = self.getPhysicalPath()
        parent_path = obj_path[len(forum_path):-1]
        
        if 'portal_factory' in obj_path:
            parent_path = parent_path[:-2]
        
        return forum.restrictedTraverse(parent_path)
    
    security.declareProtected(CMFCorePermissions.View, 'getDisplayViewVocabulary')
    def getDisplayViewVocabulary(self):
        """Returns vocabulary based on views used to display posts"""
        
        dl = DisplayList((
            ('inline', 'Inline', 'label_post_inline_view'),
            ('thread', 'Thread', 'label_post_thread_view'),
            ))
      
        return Vocabulary(dl, self, I18N_DOMAIN)
        
    security.declareProtected(CMFCorePermissions.View, 'getTopic')
    def getTopic(self):
        """
        Returns the topic post. This is the root post. 
        """
        
        depth_from_topic = self.getLevel() - 1
        if depth_from_topic == 0:
            # The post itself 
            return self
        
        topic_path = self.getPhysicalPath()[:-depth_from_topic]
        forum = self.getForum()
        return forum.restrictedTraverse(topic_path)
        
    security.declareProtected(CMFCorePermissions.View, 'isTopic')
    def isTopic(self):
        """
        Returns True if the post has a depth equals to 1
        """
        
        return (self.getLevel() == 1)

    security.declareProtected(CMFCorePermissions.View, 'isAnonymousAuthor')
    def isAnonymousAuthor(self):
        """Returns true if the author is an anonymous user"""
        
        author = self.getPostAuthor()
        return (author == 'Anonymous User')

    security.declarePrivate('_getDefaultPostAuthor')
    def _getDefaultPostAuthor(self):
        """
        Returns the author of a post.
        """
        
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        author= member.getUserName()
        return author  
        
    
    def wrapToItem(self):
        """Wrap post itself into a dictionnary

        - title: Title of post
        - url: Url of post
        - path: Path of post
        - level: Level of post
        - author: Author of post
        - anonymous: True if the author is anonymous
        - created: Creation date of post
        """
    
        item = {}
        item['title'] = self.title_or_id()
        item['url'] = self.absolute_url()
        item['path'] = '/'.join(self.getPhysicalPath())
        item['author'] = self.getPostAuthor()
        item['anonymous'] = (item['author'] == 'Anonymous User')
        item['level'] = self.getLevel()
        item['created'] = self.created()
        return item   
    
    def _wrapBrainToItem(self, brain):
        """Wrap post brain into a dictionnary

        - title: Title of post
        - url: Url of post
        - path: Path of post
        - level: Level of post
        - author: Author of post
        - anonymous: True if the author is anonymous
        - created: Creation date of post
        
        @param brain: brain from portal_catalog
        """
        
        item = {}
        item['title'] = brain['Title'] or brain['id']
        item['url'] = brain.getURL()
        item['path'] = brain.getPath()
        item['author'] = brain['getPostAuthor']
        item['anonymous'] = (item['author'] == 'Anonymous User')
        item['level'] = brain['getLevel']
        item['created'] = brain['created']
        return item   
    
    def _buildThread(self, path_to_items, path):
        """Returns a thread structure (list of items).
        Each item has this dictionnary structure:
        - title: Title of brain
        - url: Url of brain
        - path: Path of brain
        - level: Level of brain
        - created: Creation date of post
        - children: sub items
        
        @param path: path of thread we are building
        @param path_to_items: dictionnary path -> items"""
        
        # Process items in a specific path
        result = []
        items = path_to_items.get(path, [])
        
        # Loop on items
        for item in items:
            item_path = item['path']
            
            # Check if item has children
            has_children = path_to_items.has_key(item_path)
            
            # Append children
            if has_children:
                item['children'] = self._buildThread(path_to_items, item_path)
            result.append(item)
        
        return result
    
    security.declareProtected(CMFCorePermissions.View, 'wrapPostItemsInThread')
    def wrapPostItemsInThread(self, post_items):
        """Returns all post items in a thread structure.
        
        @param post_items: List of items (see _wrapBrainToItem method)
        """
        
        # Store items into a dictionnary. Key is equals to item parent path
        path_to_items = {}
        for item in post_items:
            path = item['path']
            parent_path = '/'.join(path.split('/')[:-1])
            if not path_to_items.has_key(parent_path):
                path_to_items[parent_path] = []
            path_to_items[parent_path].append(item)
        
        # Build thread
        root_path = '/'.join(self.getPhysicalPath()[:-1])
        thread = self._buildThread(path_to_items, root_path)
        return thread
    
    security.declareProtected(CMFCorePermissions.View, 'getPostItems')
    def getPostItems(self):
        """Returns all replies warp into dictionnaries."""
        
        # Get all posts contained in this post and the post itself
        obj_path = '/'.join(self.getPhysicalPath())
        query = {}
        query['path'] = obj_path
        query['sort_on'] = 'created'
        brains = self.getPostBrains(**query)
        
        # Wrap brains into readable items.
        reply_items = [self._wrapBrainToItem(x) for x in brains ]
        return reply_items
        
    security.declarePrivate('_getDefaultTitle')
    def _getDefaultTitle(self):
        """
        Returns the title of the post.
        If you reply to a post, title is a formated as 'Re: title'
        """
        
        parent = self.getParentPost()
        if parent is None:
            return ''
        
        return 'Re: %s' % parent.Title()

    security.declareProtected('View', 'getTopicPostsCount')
    def getTopicPostsCount(self):
        """
        Returns the number of posts/replies in a topic
        """

        topic = self.getTopic()
        topic_path = '/'.join(topic.getPhysicalPath())
        return (len(self.getPostBrains(path=topic_path)) - 1)
        
    security.declareProtected('View', 'getPostsCount')
    def getPostsCount(self):
        """
        Returns the number of posts/replies in a post.
        """
        
        obj_path = '/'.join(self.getPhysicalPath())
        return (len(self.getPostBrains(path=obj_path)) - 1)

    security.declareProtected('View', 'getQuotedText')
    def getQuotedText(self):
        """
        Utility method for getting the text for the quote feature
        """

        field = self.getField('text')
        quoted_text = field.get(self, raw=1)
        return quoted_text

    security.declareProtected('View', '_getDefaultText')
    def _getDefaultText(self):
        """
        Returns default text of a post.
        If user reply with quote, returns parent text as quoted.
        """
        
        request = self.REQUEST
        parent = self.getParentPost()
        if parent is None:
            # This is a topic
            return ""
        
        if not request.get('quote', False):
            # User doesn't want to quote the original post
            return ""

        return '''<div class="forumPostQuote">
                    <span class="forumPostQuoteAuthor">%s</span> - <span class="forumPostQuoteDate">%s</span>&nbsp;:
                    <blockquote>%s</blockquote>
                  </div>
                  <div>&nbsp;</div>
                  <div>&nbsp;</div>''' % (parent.getPostAuthor(), parent.Date(), parent.getQuotedText()) 

        
    ##########################
    # Catalog support
    ##########################
    
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'indexObject')
    def indexObject(self):
        """Index object in portal catalog and forum catalog"""
        BaseFolder.indexObject(self)
        cat = self.getCatalog()
        cat.indexObject(self)
    
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'unindexObject')
    def unindexObject(self):
        """Unindex object in portal catalog and forum catalog"""
        BaseFolder.unindexObject(self)
        cat = self.getCatalog()
        cat.unindexObject(self)
    
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'reindexObject')
    def reindexObject(self, idxs=[]):
        """Reindex object in portal catalog and forum catalog"""
        BaseFolder.reindexObject(self, idxs)
        cat = self.getCatalog()
        cat.reindexObject(self, idxs)

registerType(SimpleForumPost, PROJECTNAME)
