# -*- coding: utf-8 -*-
# Module providing version specific upgrade steps
import logging

from ComputedAttribute import ComputedAttribute
from zope.globalrequest import getRequest
from plone import api
from plone.app.upgrade.utils import cleanUpSkinsTool
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.component import queryUtility

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.registry.interfaces import IRegistry

default_profile = 'profile-hph.policy:default'
log = logging.getLogger(__name__)


def remove_ploneformgen(context=None, check_linkintegrity=True):
    portal = api.portal.get()
    portal_types = api.portal.get_tool('portal_types')
    portal_catalog = api.portal.get_tool('portal_catalog')
    qi = api.portal.get_tool('portal_quickinstaller')

    log.info('removing PloneFormGen')
    old_types = [
        'FormFolder',
    ]
    old_types = [i for i in old_types if i in portal_types]
    for old_type in old_types:
        for brain in portal_catalog(portal_type=old_type):
            log.info(u'Removing {}!'.format(brain.getPath()))
            api.content.delete(brain.getObject(), check_linkintegrity=check_linkintegrity)  # noqa: E501
    try:
        portal.manage_delObjects(['formgen_tool'])
    except AttributeError:
        pass
    try:
        portal.portal_properties.manage_delObjects(['ploneformgen_properties'])
    except BadRequest:
        pass

    if qi.isProductInstalled('PloneFormGen'):
        qi.uninstallProducts(['PloneFormGen'])

    if qi.isProductInstalled('Products.PloneFormGen'):
        qi.uninstallProducts(['Products.PloneFormGen'])


def migrate_ATBTreeFolder(context=None):
    """Replace very old containers for news, events and Members
    """
    from plone.portlets.interfaces import ILocalPortletAssignmentManager
    from plone.portlets.interfaces import IPortletManager
    from zope.component import getMultiAdapter
    from zope.component import queryUtility

    portal = api.portal.get()
    # create new containers:
    if not portal['Members'].__class__.__name__ == 'ATBTreeFolder':
        log.info('Migrating ATBTreeFolder not needed')
        return
    log.info('Migrating ATBTreeFolders')
    members_new = api.content.create(
        container=portal,
        type='Folder',
        id='members_new',
        title=u'Benutzer',
    )
    members_new.setOrdering('unordered')
    members_new.setLayout('@@member-search')
    # Block all right column portlets by default
    manager = queryUtility(IPortletManager, name='plone.rightcolumn')
    if manager is not None:
        assignable = getMultiAdapter(
            (members_new, manager),
            ILocalPortletAssignmentManager
        )
        assignable.setBlacklistStatus('context', True)
        assignable.setBlacklistStatus('group', True)
        assignable.setBlacklistStatus('content_type', True)


    for item in portal.Members.contentValues():
        api.content.move(
            source=item,
            target=members_new,
        )
    api.content.delete(obj=portal['Members'], check_linkintegrity=False)
    api.content.rename(obj=portal['members_new'], new_id='Members')


def uninstall_archetypes(context=None):
    portal = api.portal.get()
    request = getRequest()
    installer = api.content.get_view('installer', portal, request)
    addons = [
        'Archtypes',
        'ATContentTypes',
        'plone.app.referenceablebehavior',
        'plone.app.blob',
        'plone.app.imaging',
    ]
    for addon in addons:
        if installer.is_product_installed(addon):
            installer.uninstall_product(addon)


def remove_archetypes_traces(context=None):
    portal = api.portal.get()

    # remove obsolete AT tools
    tools = [
        'portal_languages',
        'portal_tinymce',
        'kupu_library_tool',
        'portal_factory',
        'portal_atct',
        'uid_catalog',
        'archetype_tool',
        'reference_catalog',
        'portal_metadata',
    ]
    for tool in tools:
        if tool not in portal.keys():
            log.info('Tool {} not found'.format(tool))
            continue
        try:
            portal.manage_delObjects([tool])
            log.info('Deleted {}'.format(tool))
        except Exception as e:
            log.info(u'Problem removing {}: {}'.format(tool, e))
            try:
                log.info(u'Fallback to remove without permission_checks')
                portal._delObject(tool)
                log.info('Deleted {}'.format(tool))
            except Exception as e:
                log.info(u'Another problem removing {}: {}'.format(tool, e))


def pack_database(context=None):
    """Pack the database"""
    portal = api.portal.get()
    app = portal.__parent__
    db = app._p_jar.db()
    db.pack(days=0)


def cleanup_in_plone52(context=None):
    migrate_ATBTreeFolder()
    uninstall_archetypes()
    remove_archetypes_traces()
    portal = api.portal.get()
    cleanUpSkinsTool(portal)
    qi = api.portal.get_tool('portal_quickinstaller')
    # Fix diazo theme
    qi.reinstallProducts(['plone.app.theming'])
    # Fix issue where we cannot pack the DB after it was migrated to Python 3
    qi.reinstallProducts(['plone.app.relationfield'])
    pack_database()

def fix_searchable_text(context=None):
    # Fix bytes in opkapiindex
    # See https://github.com/plone/Products.CMFPlone/issues/2905
    from Products.ZCTextIndex.interfaces import IZCTextIndex
    from Products.ZCTextIndex.interfaces import ILexicon
    catalog = api.portal.get_tool('portal_catalog')
    zctextindex = catalog._catalog.indexes['SearchableText']
    opkapiindex = zctextindex.index
    values = opkapiindex._docwords.values()
    first_item = values[0]
    if isinstance(first_item, bytes):
        log.info('Rebuilding ZCTextIndexes. First item is a byte:')
        log.info(first_item)
        lexica = [i for i in catalog.values() if ILexicon.providedBy(i)]
        for lexicon in lexica:
            lexicon.clear()

        indexes = [i for i in catalog.Indexes.objectValues()
                   if IZCTextIndex.providedBy(i)]
        for index in indexes:
            try:
                index.clear()
            except AttributeError as e:
                log.info(e)
            log.info('rebuilding {}'.format(index.__name__))
            catalog._catalog.reindexIndex(index.__name__, getRequest())
    else:
        log.info('Not rebuilding ZCTextIndexes. First item is not bytes:')
        log.info(first_item)


def fix_portlets(context=None):
    """Fix portlets that use ComputedValue for path-storage instead of a UUID.
    """
    catalog = api.portal.get_tool('portal_catalog')
    portal = api.portal.get()
    fix_portlets_for(portal)
    for brain in catalog.getAllBrains():
        try:
            obj = brain.getObject()
        except KeyError:
            log.info('Broken brain for {}'.format(brain.getPath()))
            continue
        fix_portlets_for(obj)


def fix_portlets_for(obj):
    """Fix portlets for a certain object."""
    attrs_to_fix = [
        'root_uid',
        'search_base_uid',
        'uid',
    ]
    for manager_name in ['plone.leftcolumn', 'plone.rightcolumn', 'plone.footerportlets']:
        manager = queryUtility(IPortletManager, name=manager_name, context=obj)
        if not manager:
            continue
        mappings = queryMultiAdapter((obj, manager), IPortletAssignmentMapping)
        if not mappings:
            continue
        for key, assignment in mappings.items():
            for attr in attrs_to_fix:
                if getattr(assignment, attr, None) is not None and isinstance(getattr(assignment, attr), ComputedAttribute):
                    setattr(assignment, attr, None)
                    log.info('Reset {} for portlet {} assigned at {} in {}'.format(attr, key, obj.absolute_url(), manager_name))  # noqa: E501
                    log.info('You may need to configure it manually at {}/@@manage-portlets'.format(obj.absolute_url()))  # noqa: E501


def fix_registry(context=None):
    """Remove registry-records where the interface is no longer there."""
    registry = getUtility(IRegistry)
    keys = [i for i in registry.records.keys()]
    for key in keys:
        record = registry.records[key]
        if not record.field.interface:
            # That's fine...
            continue
        try:
            iface = record.field.interface()
        except TypeError:
            # That's also fine...
            continue
        if 'broken' in str(iface):
            log.info('Removing broken record {0}'.format(key))
            del registry.records[key]


def cleanup_post_python3_migration(context=None):
    log.info('Cleanup after python3 migration')
    fix_registry()
    fix_searchable_text()
    fix_portlets()
    log.info('Plone fixes after python3 migration done')


def upgrade_1001(setup):
    # Update registry settings
    setup.runImportStepFromProfile(default_profile, 'plone.app.registry')
    # Cleanup in Plone 5.2.x
    cleanup_in_plone52()

