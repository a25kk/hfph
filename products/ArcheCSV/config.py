try:
    from Products.CMFCore.permissions import AddPortalContent
except:
    from Products.CMFCore.CMFCorePermissions import AddPortalContent

ADD_CONTENT_PERMISSION = AddPortalContent

PROJECTNAME = "ArcheCSV"

SKINS_DIR    = 'skins'

GLOBALS = globals()
