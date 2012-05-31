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
    StringField(
        name='title',
        required=1,
        searchable=1,
        default_method='getSurname',
        accessor='Title',
        widget=StringWidget(
            label='Nachname',
            label_msgid='surname',
            visible={'edit': 'visible','view' : 'invisible'},
            i18n_domain='hfph',
        ),
    ),
    StringField('Name',
                default_output_type='image/jpeg',
                widget=StringWidget(label='Vorname',i18n_domain='hfph',label_msgid='name'),
                ),
#    StringField('Surname',
#                default_output_type='image/jpeg',
#                #storage=MySQLSQLStorage(),
#                widget=StringWidget(label='Surname',i18n_domain='hfph',label_msgid='surname'),
#                ),
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
#    StringField('Country',
#                default_output_type='image/jpeg',
#                #storage=MySQLSQLStorage(),
#                widget=StringWidget(label='Country',i18n_domain='hfph',label_msgid='country'),
#                ),
#    StringField('City',
#                default_output_type='image/jpeg',
#                #storage=MySQLSQLStorage(),
#                widget=StringWidget(label='City',i18n_domain='hfph',label_msgid='city'),
#                ),
#    StringField('plz',
#                default_output_type='image/jpeg',
#                #storage=MySQLSQLStorage(),
#                widget=StringWidget(label='zip',i18n_domain='hfph',label_msgid='plz'),
#                ),
    StringField('Semester',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='Abschlusssemester (Jahreszahl)',i18n_domain='hfph',label_msgid='semester'),
                ),
#    StringField('tel',
#                default_output_type='image/jpeg',
#                #storage=MySQLSQLStorage(),
#                widget=StringWidget(label='tel',i18n_domain='hfph',label_msgid='tel'),
#                ),
    StringField('Email',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(label='e-mail',i18n_domain='hfph',label_msgid='email'),
                ),
    StringField('Comment',
                default_output_type='image/jpeg',
                #storage=MySQLSQLStorage(),
                widget=StringWidget(size=50,label='Comment',i18n_domain='hfph',label_msgid='comment'),
                ),
#    StringField('Street',
#                default_output_type='image/jpeg',
#                #storage=MySQLSQLStorage(),
#                widget=StringWidget(label='Street',i18n_domain='hfph',label_msgid='streat'),
#                ),
    ),

                              )

class anm_alumni(BaseContent):


    schema = schema
    archetype_name = "anm_alumni"

registerType(anm_alumni, PROJECTNAME)
