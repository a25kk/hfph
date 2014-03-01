from five import grok
from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.contentlisting.interfaces import IContentListing


class CleanupPublicationAuthor(grok.View):
    """ The publication Author is used to auto-link
        publications with faculty members
    """
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('cleanup-publication-author')

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
