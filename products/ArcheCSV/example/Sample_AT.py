from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.Archetypes.TemplateMixin import TemplateMixin
from Products.Archetypes.SQLStorage import MySQLSQLStorage
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except:
    from Products.CMFCore import CMFCorePermissions
from config import PROJECTNAME
from Products.LinguaPlone.public import *

schema = BaseSchema +  Schema((
    StringField('Name',
                default_output_type='image/jpeg',
                widget=StringWidget(label='Name'),
                ),
    StringField('Surname',
                default_output_type='image/jpeg',

                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='Surname'),
                ),
    StringField('Email',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='e-mail'),
                ),
    StringField('tel',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='tel'),
                ),
    ),

                              )

class Sample_AT(BaseContent):


    schema = schema
    archetype_name = "Sample_AT"

registerType(Sample_AT, PROJECTNAME)
