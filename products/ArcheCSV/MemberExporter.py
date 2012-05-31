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
import csv
import StringIO
import time

schema = Schema((
    LinesField("member_ids",
              languageIndependent = 1,
              required=True,
              schemata="Step 1: Member ids",
              default_method = "getMemberIds",
              widget = LinesWidget(
                        label = 'Member ids to export',                        
                        description = 'Please specify the member ids to export. By default, the existing member ids found in portal_memberdata are used.',
              ),
            ), 
   StringField('export_method',
              languageIndependent = 1,
              required=True,
              schemata="Step 1: Member ids",
              default='startmemberexport',
              widget=StringWidget(
                label='Export url',
                description='Python Script that is called by the export link. If in doubt leave the default setting'
                )
              ),           
   StringField("multi_valued_separator",
              languageIndependent = 1,
              schemata="Step 2: extras",
              default = ";",
              required=1,
              widget = StringWidget(
                        label = 'Separator',
                        description = 'Specify the separator used to split values used for multi-value properties as well as for roles and groups',
                        ),
              ),                 
   BooleanField("export_roles",
            schemata="Step 2: extras",
            default=True,
            widget=BooleanWidget(label="Export member roles?",
                description="Should the member roles be exported?"
                )
            ),
   BooleanField("export_groups",
            schemata="Step 2: extras",
            default=True,
            widget=BooleanWidget(label="Export groups?",
                description="Should the member groups be exported?"
                )
            ),
   BooleanField("export_password",
            schemata="Step 2: extras",
            default=True,
            widget=BooleanWidget(label="Export member passwords?",
                description="Should the member passwords be exported?"
                )
            ),
   LinesField("additional_properties",
              languageIndependent = 1,
              schemata="Step 2: extras",
              widget = LinesWidget(
                        label = 'Extra properties',
                        description = 'Extra properties, which may come from LDAP',
                        ),
              ),               
   BooleanField("stop_export_when_member_not_found",
            schemata="Step 3: define operation",
            default=True,
            widget=BooleanWidget(label="Stop export when a member to be exported can't be found?",
                description="Should the export be stopped when a member to be exported can't be found?"
                )
            ),
   BooleanField("log_property_dictionary",
            schemata="Step 3: define operation",
            default=True,
            widget=BooleanWidget(label="Log property dictionary?",
                description="Should the property dictionary of the member be logged?"
                )
            ),
   LinesField("start_export",
              languageIndependent = 1,
              schemata="Step 4: start batch export",
              widget = TextAreaWidget(
                        label = 'Start batch import',
                        macro = 'widget_startmemberexport',
                        ),
              ), 
    TextField("csv_file",
              languageIndependent = 1,
              schemata="Step 5: .csv file",
              widget = TextAreaWidget(
                        label = 'CSV file',                        
                        description = 'Consult the resulting .csv file',
                            ),
              ),
   ))
    
schema = BaseSchema + schema

class MemberExporter(BaseContent, Importer):
    
    __implements__ = BaseContent.__implements__

    schema = schema
    meta_type = portal_type = archetype_name = "Member Exporter"
    immediate_view = "exporter_edit"
    
    actions = (
        { 'id': 'view',
            'name': 'View',
            'action': 'string:${object_url}/exporter_edit',
            'permissions': (CMFCorePermissions.View,),
            'category':'object',
            },
        { 'id': 'edit',
            'name': 'Edit',
            'action': 'string:${object_url}/exporter_edit',
            'permissions': (CMFCorePermissions.View,),
            'category':'object',
            },
        
        )
    
    def getMemberIds(self):
        mtool   = getToolByName(self, 'portal_memberdata')
        return [m for m in mtool.objectIds()]
    
    def createcsv(self, headers, memberdicts):
        """ returns a csv file with member attributes
            Inspired by: http://www.zopelabs.com/cookbook/1140753093
        """
        text = StringIO.StringIO()
        writer = csv.writer(text)
        writer.writerow(headers)
        for memberdict in memberdicts:
            row = []
            for header in headers:
                row.append(memberdict[header])
            writer.writerow(row)
        self.setCsv_file(text.getvalue())  
    
    def download_csv(self):    
        """
        Returns the csv file for download
        """
        csv = self.getCsv_file()
        request = self.REQUEST
        request.RESPONSE.setHeader('Content-Type','application/csv') 
        request.RESPONSE.setHeader('Content-Length',len(csv))
        request.RESPONSE.setHeader('Content-Disposition','inline;filename=%smembers.csv' %
                                time.strftime("%Y%m%d-%H%M%S-",time.localtime()))
        return csv
            
    def get_member_password(self, member, member_id):
        acl_users = self.acl_users
        user = acl_users.getUser(name=member_id)
        try:
            password = user._getPassword()
        except:
            try:    
                password = member.getPassword()
            except:
                raise
        return password

registerType(MemberExporter, PROJECTNAME)
