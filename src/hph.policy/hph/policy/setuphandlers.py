import logging
from plone import api

PROFILE_ID = 'profile-hph.policy:default'


def setupCatalogIndexes(context, logger=None):
    """ Method to add our wanted indexes to the portal_catalog """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('hph.policy')

    setup = api.portal.get_tool(name='portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = api.portal.get_tool(name='portal_catalog')
    indexes = catalog.indexes()

    # Specify the indexes you want, with ('index_name', 'index_type')
    wanted = (('thirdPartyProject', 'FieldIndex'),
              ('academicRole', 'FieldIndex'),
              ('pubYear', 'FieldIndex'),
              ('pubMedium', 'FieldIndex'),
              ('pubSeries', 'FieldIndex'),
              ('authorLastName', 'FieldIndex'),
              )

    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def setupGroups(portal):
    acl_users = api.portal.get_tool(name='acl_users')
    if not acl_users.searchGroups(name='Staff'):
        gtool = api.portal.get_tool(name='portal_groups')
        gtool.addGroup('Staff', roles=['StaffMember'])


def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('hph.policy-various.txt') is None:
        return
    portal = api.portal.get()

    setupGroups(portal)
    setupCatalogIndexes(portal)
