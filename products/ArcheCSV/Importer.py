from Acquisition import ImplicitAcquisitionWrapper
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from config import PROJECTNAME
from Products.Archetypes.public import *
from Products.CMFCore.utils import getToolByName
import csv
import os
import sys
import traceback
from Products.Archetypes.debug import log
import logging

from StringIO import StringIO
from zipfile import ZipFile
from Products.ArcheCSV.ArcheCSVBase import ArcheCSVBase

schema = Schema((
    StringField("import_type",
              languageIndependent = 1,
              required=True,
              schemata="Step 1: choose type",
              vocabulary = "getTypes",
              widget = SelectionWidget(
						label = 'Portal type',
						description = 'Please select the portal type of the objects to import',
                        ),
              ),
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
            schemata="Step 2: upload file",
            default=True,
            widget=BooleanWidget(label="first row header",
                description='the first row contains the header information'
                )
            ),
                
   StringField('import_method',
              languageIndependent = 1,
              required=True,
              schemata="Step 2: upload file",
              default='startimport',
              widget=StringWidget(
                label='Import url',
                description='Python Script that is called by the upload link, in doubt leave the default setting'
                )
              ),

   StringField('import_target',
              languageIndependent = 1,
              schemata="Step 2: upload file",
              default='',
              widget=StringWidget(
                label='Import target',
                description='into which folder should the data be imported, if empty all objects go into portal root'
                )
              ),
              
   StringField("map_local_target",
              languageIndependent = 1,
              schemata="Step 3: map fields",
              vocabulary="get_head_selection_vocab",
              widget = SelectionWidget(
                        label = 'Map local target field',
                        description = 'Please map csv to local target field',
                        ),
              ),
   StringField("multi_valued_separator",
              languageIndependent = 1,
              schemata="Step 3: map fields",
              default = ";",
              required=1,
              widget = StringWidget(
                        label = 'Separator',
                        description = 'Specify the separator used to split values used for multi-value fields',
                        ),
              ),
   LinesField("map_zip_fields",
              languageIndependent = 1,
              schemata="Step 3: map fields",
              widget = LabelWidget(
                        label = 'Map fields',
                        description = 'Use the form below to map the fields from the csv file on the left to the AT fields on the right',
                        ),
              ),  
   LinesField("map_fields",
              languageIndependent = 1,
              schemata="Step 3: map fields",
              widget = TextAreaWidget(
                        label = 'Map fields',
                        macro = 'widget_mapchooser',
                        description = 'Please map csv to AT fields',
                        ),
              ),  
   StringField("prefix",
              languageIndependent = 1,
              schemata="Step 3: map fields",
              default="",
              widget = StringWidget(
                        label = 'prefix',                        
                        description = 'Please choose a prefix for the id of the imported objects, \
                                       the ids will be generated like this: imported.2005-11-10.113647',
                        ),
              ),                
   StringField("operation",
              languageIndependent = 1,
              required=True,
              schemata="Step 4: define operation",
              vocabulary="get_operation_vocab",
              default="add",
              widget = SelectionWidget(
                        label = 'Define operation',
                        description = 'Please define the operation',
                        ),
              ),  
   BooleanField("stop_import_when_content_not_found_on_update",
            schemata="Step 4: define operation",
            default=True,
            widget=BooleanWidget(label="Stop import when the content to be updated can't be found?",
                description="Should the import be stopped when the content to be updated can't be found?"
                )
            ),
   BooleanField("stop_import_when_content_already_exists_on_add",
            schemata="Step 4: define operation",
            default=True,
            widget=BooleanWidget(label="Stop import when the content to be added already exists?",
                description="Should the import be stopped when the content to be added alreadw exists?"
                )
            ),
   LinesField("start_import",
              languageIndependent = 1,
              schemata="Step 5: start batch import",
              widget = TextAreaWidget(
                        label = 'Start batch import',
                        macro = 'widget_startimport',
                        ),
              ), 
              
              
   ))
  

    
schema = BaseSchema + schema

class Importer(BaseContent, ArcheCSVBase):
    """Importer, an ArcheCSV component to create portal objects from CSV files"""
    __implements__ = BaseContent.__implements__
    security = ClassSecurityInfo()




    schema = schema
    meta_type = portal_type = archetype_name = "Content Importer"
    content_icon = "importer.png"
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
 
    def getTypes(self):
        at_tool=getToolByName(self,'archetype_tool')
        at_types=at_tool.listRegisteredTypes()        
        at_list=[]
        for at in at_types:
            at_list.append('%s.%s.%s' % (at['package'],at['meta_type'],at['portal_type']))
        return at_list
#    def getTypes(self):
#        at_tool=getToolByName(self,'archetype_tool')
#        at_types=at_tool.listRegisteredTypes()        
#        at_list=[]
#        for at in at_types:
#            at_list.append('%s.%s' % (at['package'],at['portal_type']))
#        return at_list

    def getArchFields(self):
        at_tool = getToolByName(self, 'archetype_tool')
        import_type = self.getImport_type()
        
        try:
            package, meta_type , portal_type  = import_type.split('.')
        except ValueError:
            #in case when portal_type isnt given
            package, meta_type = import_type.split('.')
            portal_type = meta_type
            
        types = at_tool.listRegisteredTypes()
        for t in types:
            if t['package'] != package:
                continue
                #lorty: meta_type is required for ATContentTypes
            if t['meta_type'] == meta_type:
                # We have to return the schema wrapped into the acquisition of
                # something to allow access. Otherwise we will end up with:
                # Your user account is defined outside the context of the object
                # being accessed.
                return ImplicitAcquisitionWrapper(t['schema'], self).fields()
        return None

    def getCSVheader(self):
        data=self.getCSVdata()
        return self.head
    
    
    def getCSVdata(self, file=None):
        if file:
            file_upload=file
        else:
            file_upload=self.getCsv_file()
            
        filename = self.csv_file.filename or 'untitled.csv' 

        stringio_file = StringIO(str(file_upload))
        filedatas = stringio_file.read()

        if len(filedatas) == 0:
            raise "Empty file"
        # get informations about the file
        snif = csv.Sniffer()        
        #if not snif.has_header(filedatas):
            #raise 'You must add header to the csv file!'

        #get the header
        if self.getFirstrow_header():
            rdr = csv.reader(StringIO(filedatas), snif.sniff(filedatas))
            header = rdr.next() # assume first row is header
        else:
            header=[str(h) for h in range(0,30)]

        self.head=header
            
        dialect = snif.sniff(filedatas)
        reader = csv.DictReader(StringIO(filedatas),fieldnames=header,dialect=dialect) 
        stringio_file.close() 
        return list(reader)
    
    def get_head_selection_vocab(self):
        try:
            self.head
        except:
            csvdata=self.getCSVdata()
        dl=[ ('', 'Not used') ]
        c=0
        for h in self.head:
            dl.append( (str(c), h) )
            c += 1
        return DisplayList(dl)

    security.declarePrivate('extractZipFile')
    def extractZip(self, zipFile):
        """
          Extract file in a zip
          Code taken from ZPhotoSlides product.
        """
        zip = ZipFile(zipFile,"r",8)
        file_list = {}
        for filename in zip.namelist():
            path,newfilename = os.path.split(filename)
            if newfilename[:2] != '._': ## Avoid to import OSX files
                data = zip.read(filename)
                if(len(data)):
                    file_list[newfilename] = data
        return file_list

    def get_file_from_zip(self, zip, fileName):
        filesList = self.extractZip(StringIO(zip))
        return filesList.get(fileName, None)

    def get_operation_vocab(self):
        dl = []
        dl.append( ('add', 'Only add new content') )
        dl.append( ('add_and_update', 'Add new content and update existing content') )
        dl.append( ('update', 'Only update existing content') )
        return DisplayList(dl)

registerType(Importer, PROJECTNAME)
