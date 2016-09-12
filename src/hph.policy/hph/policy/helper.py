from five import grok
from plone import api

from zope.lifecycleevent import modified

from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.contentlisting.interfaces import IContentListing

from plone.protect.interfaces import IDisableCSRFProtection

from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds

from hph.faculty.facultymember import IFacultyMember

from hph.lectures.lecture import ILecture
from hph.publications.publicationfolder import IPublicationFolder
from hph.publications.publication import IPublication


class CleanupView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('cleanup-view')


class CleanupPublicationSchema(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('cleanup-publications')

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        return self.render()

    def update(self):
        self.has_publications = len(self.publications()) > 0

    def render(self):
        idx = self._cleanup_schema()
        return 'Cleaned up {0} publications'.format(idx)

    def _cleanup_schema(self):
        items = self.publications()
        idx = 0
        for item in items:
            obj = item.getObject()
            third_party_project = getattr(obj, 'thirdPartyProject', None)
            if third_party_project:
                external_funds = list(third_party_project)
                setattr(obj, 'externalFundsProject', external_funds)
            idx += 1
            modified(obj)
            obj.reindexObject(idxs=['externalFundsProject', 'modified'])
        return idx

    def publications(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        results = catalog(object_provides=IPublication.__identifier__,)
        return IContentListing(results)


class CleanupLecturesSchema(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('cleanup-lectures')

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        return self.render()

    def update(self):
        self.has_lectures = len(self.lectures()) > 0

    def render(self):
        idx = self._cleanup_schema()
        return 'Cleaned up {0} objects'.format(idx)

    def _cleanup_schema(self):
        items = self.lectures()
        idx = 0
        for item in items:
            obj = item.getObject()
            third_party_project = getattr(obj, 'thirdPartyProject', None)
            if third_party_project:
                external_funds = list(third_party_project)
                setattr(obj, 'externalFundsProject', external_funds)
            idx += 1
            modified(obj)
            obj.reindexObject(idxs=['externalFundsProject', 'modified'])
        return idx

    def lectures(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        results = catalog(object_provides=ILecture.__identifier__,)
        return IContentListing(results)

    def get_relations(self, obj, attribute=None, backrefs=False):
        """Get any kind of references and backreferences"""
        int_id = self.get_intid(obj)
        if not int_id:
            return retval

        relation_catalog = getUtility(ICatalog)
        if not relation_catalog:
            return retval

        query = {}
        if attribute:
            # Constrain the search for certain relation-types.
            query['from_attribute'] = attribute

        if backrefs:
            query['to_id'] = int_id
        else:
            query['from_id'] = int_id

        return relation_catalog.findRelations(query)

    def get_intid(self, obj):
        """Return the intid of an object from the intid-catalog"""
        intids = queryUtility(IIntIds)
        if intids is None:
            return
        # check that the object has an intid, otherwise there's nothing to be done
        try:
            return intids.getId(obj)
        except KeyError:
            # The object has not been added to the ZODB yet
            return


class CleanupFacultyMemberSchema(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('cleanup-facultymembers')

    def render(self):
        idx = self._cleanup_schema()
        return 'Cleaned up {0} faculty members'.format(idx)

    def _cleanup_schema(self):
        items = self.items()
        idx = 0
        for item in items:
            i = item.getObject()
            author_name = getattr(i, 'last_name')
            setattr(i, 'lastname', author_name)
            idx += 1
            modified(i)
            i.reindexObject(idxs='modified')
        return idx

    def items(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        results = catalog(object_provides=IFacultyMember.__identifier__,
                          sort_on='getObjPositionInParent')
        return IContentListing(results)


class AutoCleanupFiles(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('cleanup-files')

    def render(self):
        idx = 0
        for item in self.to_cleanup():
            api.content.delete(obj=item.getObject())
            idx += 1
        msg = 'File and images removed: {0}'.format(idx)
        return msg

    def to_cleanup(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        ptypes = ['Image', 'File']
        results = catalog(portal_type=ptypes)
        items = IContentListing(results)
        return items
