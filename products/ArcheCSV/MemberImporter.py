from AccessControl.SecurityManagement import newSecurityManager
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions
from config import PROJECTNAME
from Products.Archetypes.public import *
from Products.CMFCore.utils import getToolByName
import csv
import os
from StringIO import StringIO
from Importer import Importer
from Products.CMFCore.utils  import getToolByName
from AccessControl.SecurityManager import setSecurityPolicy
from Products.CMFCore.tests.base.security import OmnipotentUser
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy
from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.debug import log
import logging

try:
    from Products.remember.utils import getAdderUtility
    REMEMBER_INSTALLED=True
except ImportError:
    REMEMBER_INSTALLED=False

class PSOmnipotentUser(OmnipotentUser):
    # Need this method to assign groups to users
    def has_permission(self, permission, object):
        return True

schema = Schema((
   TextField("csv_file",
              languageIndependent = 1,
              required=True,
              schemata="Step 2: upload file",
              allowable_content_types= ('text/comma-separated-values',),
              widget = RichWidget(
                        rows=15,
                        cols=50,          
                        label = 'CSV file', 
                        visible = {'view':'invisible','edit':'visible'}, 
                        description = 'Please upload a CSV file containing field values for the objects to create,\
                                       here you will see a preview of the content',
                        allow_file_upload=True,
                        helper_css = ('archecsv.css',),
                            ),
              ), 
   BooleanField("firstrow_header",
            schemata="Step 1: upload file",
            default=True,
            widget=BooleanWidget(label="first row header",
                description='the first row contains the header information'
                )
            ),
                
   StringField('import_method',
              languageIndependent = 1,
              required=True,
              schemata="Step 1: upload file",
              default='startmemberimport',
              widget=StringWidget(
                label='Import url',
                description='Python Script that is called by the upload link, in doubt leave the default setting'
                )
              ),
   StringField("multi_valued_separator",
              languageIndependent = 1,
              schemata="Step 2: map fields",
              default = ";",
              required=1,
              widget = StringWidget(
                        label = 'Separator',
                        description = 'Specify the separator used to split values used for multi-value properties as well as for roles and groups',
                        ),
              ),
   StringField("map_login_field",
              languageIndependent = 1,
              schemata="Step 2: map fields",
              vocabulary="get_head_selection_vocab",
              widget = SelectionWidget(
                        label = 'Map login field',
                        description = 'Please map csv to login field',
                        ),
              ),  
   StringField("map_role_field",
              languageIndependent = 1,
              schemata="Step 2: map fields",
              vocabulary="get_head_selection_vocab",
              widget = SelectionWidget(
                        label = 'Map role field',
                        description = 'Please map csv to role field',
                        ),
              ),  
   StringField("map_group_field",
              languageIndependent = 1,
              schemata="Step 2: map fields",
              vocabulary="get_head_selection_vocab",
              widget = SelectionWidget(
                        label = 'Map group field',
                        description = 'Please map csv to group field',
                        ),
              ),  
   StringField("map_password_field",
              languageIndependent = 1,
              schemata="Step 2: map fields",
              vocabulary="get_head_selection_vocab",
              widget = SelectionWidget(
                        label = 'Map Password field',
                        description = 'Please map csv to password field',
                        ),
              ),  
   LinesField("map_fields",
              languageIndependent = 1,
              schemata="Step 2: map fields",
              widget = TextAreaWidget(
                        label = 'Map fields',
                        macro = 'widget_memberdatamapchooser',
                        description = 'Please map csv to memberdata fields',
                        ),
              ),  
   StringField("operation",
              languageIndependent = 1,
              required=True,
              schemata="Step 3: define operation",
              vocabulary="get_operation_vocab",
              default="add",
              widget = SelectionWidget(
                        label = 'Define operation',
                        description = 'Please define the operation',
                        ),
              ),  
   BooleanField("stop_import_when_member_not_found_on_update",
            schemata="Step 3: define operation",
            default=True,
            widget=BooleanWidget(label="Stop import when a member to be updated can't be found?",
                description="Should the import be stopped when a member to be updated can't be found?"
                )
            ),
   BooleanField("stop_import_when_member_already_exists_on_add",
            schemata="Step 3: define operation",
            default=True,
            widget=BooleanWidget(label="Stop import when a member to be added already exists?",
                description="Should the import be stopped when a member to be added alreadw exists?"
                )
            ),
   BooleanField("create_groups_implicitly",
            schemata="Step 3: define operation",
            default=True,
            widget=BooleanWidget(label="Should groups be added implicitly?",
                description="Check this option if you want groups that are specified for the user but not yet created in the portal become created for you"
                )
   
   ),
   LinesField("start_import",
              languageIndependent = 1,
              schemata="Step 4: start batch import",
              widget = TextAreaWidget(
                        label = 'Start batch import',
                        macro = 'widget_startmemberimport',
                        ),
              ), 
              
   ))
    
schema = BaseSchema + schema

class MemberImporter(BaseContent, Importer):
    
    __implements__ = BaseContent.__implements__

    schema = schema
    meta_type = portal_type = archetype_name = "Member Importer"
    immediate_view = "importer_edit"
    
    actions = (
        { 'id': 'view',
            'name': 'View',
            'action': 'string:${object_url}/importer_edit',
            'permissions': (CMFCorePermissions.View,),
            'category':'object',
            },
        { 'id': 'edit',
            'name': 'Edit',
            'action': 'string:${object_url}/importer_edit',
            'permissions': (CMFCorePermissions.View,),
            'category':'object',
            },
        
          )

    def setMemberProperties(self, member, properties):
        member.setMemberProperties(properties)

        
    def getMemberPropertyIds(self):
        mdtool=self.portal_memberdata

        try:
            #heuristics: if the following fails, we assume that remember isnt installed
            adder = getAdderUtility(self)
            
            try:
                mtype=adder.default_member_type
            except AttributeError:
                #if we dont have a defined default member type lets take Member
                mtype='Member' 

            att=self.archetype_tool
            for td in att.listRegisteredTypes():
                if td['name']==mtype:
                    schema=td['schema']
                    break
            return [f.getName() for f in schema.fields()]
        except:
            #fallback if remember isnt installed
            return mdtool.propertyIds()

    def setMemberGroups(self, login, groups):
        """checks the existence of groups and if not present creates these groups"""
        pg = getToolByName(self, 'portal_groups')
        for groupname in groups:
            if groupname != "":
                group = pg.getGroupById(groupname)
                if group is None:
                    if self.getCreate_groups_implicitly():
                        pg.addGroup(groupname)
                        group = pg.getGroupById(groupname)
                    else:
                        raise "Unknown group: %s" % groupname
                group.addMember(login)


    def addMember(self, login, properties, roles=[], groups=[], password=None):
        
        pu = getToolByName(self, 'portal_url')
        pr = getToolByName(self, 'portal_registration')
        portal = pu.getPortalObject()
        if not password:
            password = pr.generatePassword()

        if not properties.has_key('username'):
            properties['username'] = login
        if not properties.has_key('email'):
            properties['email'] = 'example@example.com'

        # Using a technique to become omnipotent user taken from:
        # http://zopelabs.com/cookbook/1091472367
        # This is necessarry in order to be able to add users even
        # when the tests are called by anonymous
        _policy=PermissiveSecurityPolicy()
        _oldpolicy=setSecurityPolicy(_policy)
        newSecurityManager(None, PSOmnipotentUser().__of__(portal.acl_users))

        pr.addMember(id=login, password=password, roles=roles, properties=properties)
        self.setMemberGroups(login,groups)
        setSecurityPolicy(_oldpolicy)

        log('MemberImporter', logging.INFO, 'login: %s roles: %s groups: %s' %(login, str(roles), str(groups)))

    def updateMember(self, login, properties, roles=[], groups=[],):
        """ Updates a member """
        pm = getToolByName(self, 'portal_membership')
        pr = getToolByName(self, 'portal_registration')
        pu = getToolByName(self, 'portal_url')
        portal = pu.getPortalObject()

        # Using a technique to become omnipotent user taken from:
        # http://zopelabs.com/cookbook/1091472367
        # This is necessarry in order to be able to add users even
        # when the tests are called by anonymous
        _policy=PermissiveSecurityPolicy()
        _oldpolicy=setSecurityPolicy(_policy)
        newSecurityManager(None, PSOmnipotentUser().__of__(portal.acl_users))
        self.setMemberGroups(login, groups)
        member = pm.getMemberById(login)
        member.setMemberProperties(properties)
        self.acl_users.userFolderEditUser(login, None, roles, member.getDomains())
        log('MemberImporter', logging.INFO, 'login: %s roles: %s groups: %s' %(login, str(roles), str(groups)))

        #pr.editMember(member_id=login,
        #              roles=roles,
        #              properties=properties)

        setSecurityPolicy(_oldpolicy)

    def get_operation_vocab(self):
        dl = []
        dl.append( ('add', 'Only add new users') )
        dl.append( ('add_and_update', 'Add new users and update existing users') )
        dl.append( ('update', 'Only update existing users') )
        return DisplayList(dl)

registerType(MemberImporter, PROJECTNAME)
