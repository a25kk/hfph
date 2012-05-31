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
#    StringField(
#        name='title',
#        required=1,
#        searchable=1,
#        default_method='getSurname',
#        accessor='Title',
#        widget=StringWidget(
#            label='Surname',
#            label_msgid='surname',
#            visible={'edit': 'visible','view' : 'invisible'},
#            i18n_domain='hfph',
#        ),
#    ),
    StringField('Name',
                default_output_type='image/jpeg',
                widget=StringWidget(label='Name',i18n_domain='hfph',label_msgid='name'),
                ),
    StringField('Surname',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='Surname',i18n_domain='hfph',label_msgid='surname'),
                ),
    StringField('akTitle',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='Title',i18n_domain='hfph',label_msgid='ak_title'),
                ),
#    StringField('Profession',
#                default_output_type='image/jpeg',
#                #storage=MySQLSQLStorage(),
#                widget=StringWidget(label='profession',i18n_domain='hfph',label_msgid='profession'),
#                ),
    StringField('Country',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='Country',i18n_domain='hfph',label_msgid='country'),
                ),
    StringField('City',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='City',i18n_domain='hfph',label_msgid='city'),
                ),
    StringField('plz',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='zip',i18n_domain='hfph',label_msgid='plz'),
                ),
    StringField('tel',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='tel',i18n_domain='hfph',label_msgid='tel'),
                ),
    StringField('Email',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='e-mail',i18n_domain='hfph',label_msgid='email'),
                ),
    StringField('Street',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='Street',i18n_domain='hfph',label_msgid='streat'),
                ),
    ),

                              )

class d_alumni(BaseContent):


    schema = schema
    archetype_name = "d_alumni"

registerType(d_alumni, PROJECTNAME)
