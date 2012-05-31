from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.ArcheCSV.config import PROJECTNAME, GLOBALS, SKINS_DIR

from StringIO import StringIO

def install(self):
    out = StringIO()

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    out.write("Successfully installed %s." % PROJECTNAME)
    return out.getvalue()
