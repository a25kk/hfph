#from Products.Archetypes.Marshall import PrimaryFieldMarshaller
#from Products.Archetypes.TemplateMixin import TemplateMixin
#from Products.Archetypes.TemplateMixin import TemplateMixin
from Acquisition import ImplicitAcquisitionWrapper
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

schema = Schema((

   StringField("target_type",
              languageIndependent = 1,
              schemata="Step1: choose types",
              vocabulary = "getTypes",
              widget = SelectionWidget(
						label = 'Portal type',
						description = 'Please select the SOURCE portal type (the reference will be set from this portal type, must have at least one ReferenceField, e.g. ATDocument)',
                        #macro = "widget_typeschooser",
                        ),
              ),
   FileField("csv_file",
              languageIndependent = 1,
              schemata="Step2: upload file",
              allowable_content_types= ('text/comma-separated-values',),
              default = "source_id,target_id\nwedding,img1\nwedding,img2", 
              widget = RichWidget(
                        rows=15,
                        cols=50,          
                        label = 'CSV file',     
                        description = 'Please upload a CSV file containing the source_id, target_id header and field values for the objects to reference,\
                                       here you will see a preview of the content',
                        helper_css = ('archecsv.css',),
                        ),
              ),  
   StringField("map_fields",
              languageIndependent = 1,
              schemata="Step3: map fields",
              widget = StringWidget(
                        label = 'Map fields',
                        macro = 'widget_relchooser',
                        description = 'Please map csv to AT fields',
                        ),
              ),  

   LinesField("start_import",
              languageIndependent = 1,
              schemata="Step4: start batch import",
              widget = TextAreaWidget(
                        label = 'Start batch import',
                        macro = 'widget_rel_startimport',
                        ),
              ),
                 ))
  


schema = BaseSchema + schema

class Refmaker(BaseContent):
    """Reference maker, an ArcheCSV component to create references between portal objects"""
    __implements__ = BaseContent.__implements__
    
    def getTypes(self):
        at_tool=getToolByName(self,'archetype_tool')
        at_types=at_tool.listRegisteredTypes()        
        at_list=[]
        for at in at_types:
            at_list.append('%s.%s' % (at['package'],at['name']))
        return at_list



    schema = schema
    meta_type = portal_type = archetype_name = "Reference maker"
    immediate_view = "refmaker_edit"
    content_icon = "refmaker.png"
    description = "Reference maker"
    
    actions = (
        { 'id': 'view',
            'name': 'View',
            'action': 'string:${object_url}/refmaker_edit',
            'permissions': (CMFCorePermissions.View,),
            'category':'object',
            },
        { 'id': 'edit',
            'name': 'Edit',
            'action': 'string:${object_url}/refmaker_edit',
            'permissions': (CMFCorePermissions.View,),
            'category':'object',
            },
        
          )
 
 
    def getArchFields(self):
        at_tool = getToolByName(self, 'archetype_tool')
        import_type = self.getTarget_type()
        package, portal_type = import_type.split('.')
        types = at_tool.listRegisteredTypes()
        for t in types:
            if t['package'] != package:
                continue
            #lorty: meta_type is required for ATContentTypes
            if t['meta_type'] == portal_type:
                # We have to return the schema wrapped into the acquisition of
                # something to allow access. Otherwise we will end up with:
                # Your user account is defined outside the context of the object
                # being accessed.
                return ImplicitAcquisitionWrapper(t['schema'], self).fields()
        return None


    def getCSVheader(self):
        data=self.getCSVdata()
        return self.head
    
    
    def getCSVdata(self):
        file_upload=self.getCsv_file()
        filename = file_upload.filename 
        #raise filename     
        stringio_file = StringIO(str(file_upload))
        filedatas = stringio_file.read()
        
        
        #var_directory = self.Control_Panel.getCLIENT_HOME()

        # get informations about the file
        snif = csv.Sniffer()        
        #if not snif.has_header(filedatas):
            #raise 'You must add header to the csv file!'

        #get the header
        rdr = csv.reader(StringIO(filedatas), snif.sniff(filedatas))
        header = rdr.next() # assume first row is header
        self.head=header
        
        dialect = snif.sniff(filedatas)

        # first, create a temp file on file system
        #self._createTempFile(var_directory, filename, filedatas)

        # open temp csv file
        #reader = csv.DictReader(open('%s/%s' % (var_directory, filename)), dialect=dialect)

        reader = csv.DictReader(StringIO(filedatas),fieldnames=header,dialect=dialect)
        stringio_file.close() 
        return list(reader)
    

registerType(Refmaker, PROJECTNAME)
