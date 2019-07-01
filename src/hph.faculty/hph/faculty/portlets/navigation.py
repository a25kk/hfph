# -*- coding: utf-8 -*-
"""Module providing faculty content navigation"""
from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from hph.faculty.facultymember import IFacultyMember
from hph.sitecontent.contentpage import IContentPage
from plone import api
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from hph.faculty import MessageFactory as _


class IFacultyNavigationPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFacultyNavigationPortlet)

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _("Faculty Navigation")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('navigation.pt')

    @property
    def available(self):
        return True

    def has_content_items(self):
        return len(self.content_items()) > 0

    def has_content_links(self):
        return len(self.content_links()) > 0

    def has_publications(self):
        if self.faculty_member():
            # check for publication content
            try:
                content = self.faculty_member().associatedPublications
            except AttributeError:
                content = None
            if content is not None:
                return True
        return False

    def content_items(self):
        items = list()
        if self.faculty_member():
            documents = api.content.find(
                context=self.faculty_member(),
                depth=2,
                object_provides=IContentPage,
                review_state="published",
                sort_on="getObjectPositionInParent"
            )
            for brain in documents:
                items.append({
                    "title": brain.Title,
                    "url": brain.getURL(),
                })
        return items

    def content_links(self):
        items = list()
        if self.faculty_member():
            links = api.content.find(
                context=self.faculty_member(),
                depth=1,
                portal_type="Link",
                review_state="published",
                sort_on="getObjectPositionInParent"
            )
            for brain in links:
                items.append({
                    "title": brain.Title,
                    "url": brain.getURL(),
                })
        return items

    def faculty_member(self):
        context = aq_inner(self.context)
        assignment_context = self._assignment_context()
        if IFacultyMember.providedBy(context):
            return context
        chain = self._get_acquisition_chain(context)
        for content_item in chain:
            if IFacultyMember.providedBy(content_item):
                return content_item
        return None

    def _assignment_context(self):
        context = aq_inner(self.context)
        assignment_context_path = self.__portlet_metadata__['key']
        assignment_context = context.restrictedTraverse(
            assignment_context_path
        )
        return assignment_context

    @staticmethod
    def _get_acquisition_chain(context_object):
        """
        @return: List of objects from context, its parents to the portal root

        Example::

            chain = getAcquisitionChain(self.context)
            print "I will look up objects:" + str(list(chain))

        @param object: Any content object
        @return: Iterable of all parents from the direct parent to the site root
        """

        # It is important to use inner to bootstrap the traverse,
        # or otherwise we might get surprising parents
        # E.g. the context of the view has the view as the parent
        # unless inner is used
        inner = context_object.aq_inner

        content_node = inner

        while content_node is not None:
            yield content_node

            if ISiteRoot.providedBy(content_node):
                break
            if not hasattr(content_node, "aq_parent"):
                raise RuntimeError(
                    "Parent traversing interrupted by object: {}".format(
                        str(content_node)
                    )
                )
            content_node = content_node.aq_parent


class AddForm(base.AddForm):
    """Portlet add form.
    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    schema = IFacultyNavigationPortlet

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    schema = IFacultyNavigationPortlet
