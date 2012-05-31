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
$Id: Install.py 5411 2006-08-30 08:30:18Z clebeaupin $
"""
__author__  = 'Jerome Sandarnaud'
__docformat__ = 'restructuredtext'

# Python imports
from StringIO import StringIO

# CMF imports
#from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.CMFCore.utils import getToolByName

# Archetypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes

# Product import
from Products.SimpleForum.config import PROJECTNAME, GLOBALS, SKINS_DIR, TOOL_ID
#rom Products.SimpleForum.Extensions.installWorkflows import createSimpleforum_workflow, createSimplepost_workflow
from Products.SimpleForum import permissions
from Products.SimpleForum.tool import SimpleForumTool

#def addWorkflow(self, wf_id, wf_title, method, portal_types):
#    """
#    add a workflow to portal_workflow
#    """
#    wtool = getToolByName(self, 'portal_workflow')
#    addWorkflowFactory(method,
#                       id=wf_id,
#                       title=wf_title)
#    wtool.manage_addWorkflow('%s (%s)' % (wf_id, wf_title), wf_id)
#    wtool.setChainForPortalTypes(portal_types, wf_id)

#ef setupWorkflows(self, out):
#   """
#   Install SimpleForum Workflows
#   SimpleForum and SimpleForumPost objects have their own workflows
#   """
#   wtool = getToolByName(self, 'portal_workflow')
#   addWorkflow(self, 
#               wf_id='simpleforum_workflow',
#               wf_title='Simple Forum workflow',
#               method=createSimpleforum_workflow,
#               portal_types=('SimpleForum',))
                
#   addWorkflow(self,
#               wf_id='simpleforumpost_workflow',
#               wf_title='Simple Forum Post workflow',
#               method=createSimplepost_workflow,
#               portal_types=('SimpleForumPost',))
    
#   wtool.setChainForPortalTypes(('SimpleForumFolder',), 'folder_workflow')
#   print >> out, 'Workflow installed'


def registerTypesForFactory(self, out, types):
    """
    Register types with portal_factory
    """
    factory = getToolByName(self, 'portal_factory')
    registered = factory.getFactoryTypes().keys()
    for type in types:
        if type not in registered:
            registered.append(type)
    factory.manage_setPortalFactoryTypes(listOfTypeIds = registered)
    print >> out, "Registered new types to portal_factory"


def installTool(self, out):
    """Install SimpleForum tool"""
    
    tool = getToolByName(self, TOOL_ID, None)
    
    if tool is None:
        #Add the tool
        add_tool = self.manage_addProduct[PROJECTNAME].manage_addTool
        add_tool(SimpleForumTool.meta_type)
        tool = getToolByName(self, TOOL_ID)
        print >>out, 'SimpleForum tool installed.\n'

def install(self):
    """Install PloneSimpleForum product"""
    out = StringIO()
    # Install types and "switch" external methods
    typeInfo = listTypes(PROJECTNAME)
    installTypes(self, out, typeInfo, PROJECTNAME)
    
    # Install skin
    install_subskin(self, out, GLOBALS)
    
    # Permissions for Plone roles
    self.manage_permission(permissions.AddSimpleForumPost, ('Member', 'Owner', 'Manager'), 1)
    
    # Add workflows
#    setupWorkflows(self, out)
    
    # Register Post type w/ portal_factory
    registerTypesForFactory(self, out, ('SimpleForumFolder', 'SimpleForum', 'SimpleForumPost',))
    
    provider = getToolByName(self, 'portal_selenium', None)
    if provider:
        # Functional Tests
        action = {'id':PROJECTNAME.lower(),
                  'name':PROJECTNAME,
                  'action':'string:here/get_%s_ftests'%PROJECTNAME.lower(),
                  'condition': '',
                  'permission': 'View',
                  'category':'ftests',
                  'visible': 1}
        provider.addAction(**action)

    typesTool = getToolByName(self, 'portal_types')
    
    # Set the human readable title explicitly
    t = getattr(typesTool, 'SimpleForum', None)
    if t:
        t.title = 'Forum'

    # Install tool
    installTool(self, out)

    out.write('Installation completed.\n')
    return out.getvalue()

def uninstall(self):
    """Uninstall PloneGlossary product"""
    out = StringIO()
    out.write('Uninstallation completed.\n')
    return out.getvalue()
