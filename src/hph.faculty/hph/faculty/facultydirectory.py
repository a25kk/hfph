from Acquisition import aq_inner
from five import grok
from plone import api

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable

from hph.faculty.facultymember import IFacultyMember

from hph.faculty import MessageFactory as _


class IFacultyDirectory(form.Schema, IImageScaleTraversable):
    """
    A directory of faculty staff members
    """


class FacultyDirectory(Container):
    grok.implements(IFacultyDirectory)


class View(grok.View):
    grok.context(IFacultyDirectory)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.filter = self.request.get('content_filter', '')

    def filtered(self):
        return self.filter is True

    def faculty_members(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        query = self._base_query()
        if self.filter:
            query['position'] = self.filter
        results = catalog(query)
        return results

    def _base_query(self):
        context = aq_inner(self.context)
        obj_provides = IFacultyMember.__identifier__
        query_path = dict(query='/'.join(context.getPhysicalPath()),
                          depth=1),
        return dict(object_provides=obj_provides,
                    path=query_path,
                    review_state='published')
