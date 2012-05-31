from Globals import package_home

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory



from config import SKINS_DIR, GLOBALS, PROJECTNAME
from config import ADD_CONTENT_PERMISSION

registerDirectory(SKINS_DIR, GLOBALS)

from Products.PythonScripts.Utility import allow_module
allow_module('csv')

def initialize(context):
    ##Import Types here to register them
    import Importer
#    import Exporter
#    import MemberImporter
#    import MemberExporter
#    import Refmaker
    import d_alumni
    import alumni
    import anm_alumni

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
