import csv
import os
import csv
import time
import StringIO
from Products.ArcheCSV.ArcheCSVBase import ArcheCSVBase
from Products.CMFCore.utils import getToolByName
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions

from Products.Archetypes.public import *

from config import PROJECTNAME

from csv import Dialect
from csv import QUOTE_NONE

class excel_tab_quote_none(Dialect):
    delimiter = '\t'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_NONE
    escapechar = "\\"

schema = Schema((
    StringField("export_type",
              languageIndependent = 1,
              required=True,
              schemata="Step 1: configuration",
              vocabulary = "getTypes",
              widget = SelectionWidget(
              label = 'Portal type',
              description = 'Please select the portal type of the objects to export',
                        ),
              ),
   StringField('export_method',
              languageIndependent = 1,
              required=True,
              schemata="Step 1: configuration",
              default='startexport',
              widget=StringWidget(
                label='Import url',
                description='Python Script that is called by the export link, in doubt leave the default setting'
                )
              ),
   StringField("multi_valued_separator",
              languageIndependent = 1,
              schemata="Step 1: configuration",
              default = ";",
              required=1,
              widget = StringWidget(
                        label = 'Separator',
                        description = 'Specify the separator used to split values used for multi-value properties',
                        ),
              ),
   BooleanField("stop_export_when_content_not_found",
            schemata="Step 2: define operation",
            default=True,
            widget=BooleanWidget(label="Stop export when a content to be exported can't be found?",
                description="Should the export be stopped when a content to be exported can't be found?"
                )
            ),
   BooleanField("log_property_dictionary",
            schemata="Step 2: define operation",
            default=True,
            widget=BooleanWidget(label="Log property dictionary?",
                description="Should the property dictionary of the content be logged?"
                )
            ),
   LinesField("start_export",
              languageIndependent = 1,
              schemata="Step 3: start batch export",
              widget = TextAreaWidget(
                        label = 'Start batch import',
                        macro = 'widget_startexport',
                        ),
              ), 
    TextField("csv_file",
              languageIndependent = 1,
              schemata="Step 3: .csv file",
              widget = TextAreaWidget(
                        label = 'CSV file',
                        description = 'Consult the resulting .csv file',
                            ),
              ),
   ))

schema = BaseSchema + schema


class ContentExporter(BaseContent, ArcheCSVBase):
    
    __implements__ = BaseContent.__implements__

    schema = schema
    meta_type = portal_type = archetype_name = "Content Exporter"
    immediate_view = "content_exporter_edit"
    
    actions = (
        { 'id': 'view',
            'name': 'View',
            'action': 'string:${object_url}/content_exporter_edit',
            'permissions': (CMFCorePermissions.View,),
            'category':'object',
            },
        { 'id': 'edit',
            'name': 'Edit',
            'action': 'string:${object_url}/content_exporter_edit',
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

    def createcsv(self, headers, contentdicts):
        """ returns a csv file with content information
            Inspired by: http://www.zopelabs.com/cookbook/1140753093
        """
        text = StringIO.StringIO()
        csv.register_dialect("excel_tab_quote_none", excel_tab_quote_none)
        writer = csv.writer(text, "excel_tab_quote_none")
        writer.writerow(headers)
        for contentdict in contentdicts:
            row = []
            for header in headers:
                row.append(contentdict[header])
            writer.writerow(row)
        self.setCsv_file(text.getvalue())
    
    def download_csv(self):
        """
        Returns the csv file for download
        """
        csv = self.getField("csv_file").getBaseUnit(self, full=True)
        request = self.REQUEST
        request.RESPONSE.setHeader('Content-Type','application/csv') 
        request.RESPONSE.setHeader('Content-Length',len(csv))
        request.RESPONSE.setHeader('Content-Disposition','inline;filename=%scontent.csv' %
                                time.strftime("%Y%m%d-%H%M%S-",time.localtime()))
        return csv

    #
    # export handlers taken from ArchXMLTool
    # https://svn.plone.org/svn/archetypes/ArchXMLTool/trunk
    #
    def normalize_field(self, field):
        return field.__class__.__name__.lower()
        
    def stringfield_export(self, instance, field, contentdict):
        accessor = field.getAccessor(instance)
        value = accessor and accessor()
        if not value:
            contentdict[field.getName()]=""
        else:
            assert type(value) is type(''), '%s: %s instead of string' % (field.getName(),field.type)
            contentdict[field.getName()]=value

    def linesfield_export(self, instance, field, contentdict):
        accessor = field.getEditAccessor(instance)
        value = self.getMulti_valued_separator().join(accessor())
        if not value:
            contentdict[field.getName()]=""
        else:
            contentdict[field.getName()]=value

    def datetimefield_export(self, instance, field, contentdict):
        accessor = field.getEditAccessor(instance)
        value = str(accessor())
        contentdict[field.getName()]=value

    def compoundfield_export(self, instance, field, contentdict):
        accessor = field.getEditAccessor(instance)
        value = str(accessor())
        contentdict[field.getName()]=value

    def arrayfield_export(self, instance, field, contentdict):
        accessor = field.getEditAccessor(instance)
        value = str(accessor())
        contentdict[field.getName()]=value

    def computedfield_export(self, instance, field, contentdict):
        accessor = field.getAccessor(instance)
        contentdict[field.getName()]=str(accessor())

    def referencefield_export(self, instance, field, contentdict):
        accessor  = field.getEditAccessor(instance)
        uid = accessor()
        utool = getToolByName(self, "uid_catalog")
        brains = utool(UID=uid)
        targets = []
        for brain in brains:
            targets.append(brain.getObject().Title())
        contentdict[field.getName()]=", ".join(targets)

    def filefield_export(self, instance, field, contentdict):
        value = field.getBaseUnit(instance, full=True)
        filename = value.filename
        contentdict[field.getName()]=str(filename)

    def textfield_export(self, instance, field, contentdict):
        accessor = field.getEditAccessor(instance)
        value = accessor(raw=1)
        if hasattr(value, 'original_encoding'):
            encoding = value.original_encoding.lower()
        else:
            encoding = 'ascii'
        _value = value.getRaw(encoding=encoding)
        _value = _value.replace(chr(10), " ")
        contentdict[field.getName()] = _value

    defaultfield_export = stringfield_export

registerType(ContentExporter, PROJECTNAME)
