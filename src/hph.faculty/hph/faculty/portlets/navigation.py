# -*- coding: utf-8 -*-
"""Module providing faculty content navigation"""
from zope.interface import implementer

from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone import utils
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import implementer

from hph.faculty import MessageFactory as _
from hph.faculty.facultymember import IFacultyMember
from hph.sitecontent.contentpage import IContentPage


class IFacultyNavigationPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

@implementer(IFacultyNavigationPortlet)
class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

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

    _nav_tree = None

    _item_markup_template = (
        u'<li class="c-nav-list__item {id}{has_sub_class}">'
        u'<a href="{url}" class="c-nav-list__link c-nav-list__link--state-{review_state}{active_class}">{title}</a>'  # noqa: E 501
        u'{sub}'
        u'</li>'
    )
    _subtree_markup_wrapper = (
        u'<ul class="c-nav-list c-nav-list--level-1 c-nav-list__subtree">{out}</ul>'  # noqa: E 501
    )

    render = ViewPageTemplateFile('navigation.pt')

    @property
    def available(self):
        return self.faculty_member()

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

    def static_view_is_active(self, view_name):
        url = self.request["URL"]
        if url.endswith(view_name):
            return True
        return False

    @property
    def nav_tree(self):

        if self._nav_tree is not None:
            return self._nav_tree

        types = ['hph.sitecontent.contentpage', 'Link', ]
        lang_current = api.portal.get_current_language()

        query = {
            'path': {
                'query': '/'.join(self.faculty_member().getPhysicalPath()),
                'depth': 2
            },
            'portal_type': {'query': types},
            'review_state': 'published',
            'Language': lang_current,
            'sort_on': 'getObjPositionInParent'
        }
        brains = api.content.find(**query)

        ret = {}

        # Get current object path for later determine if it's current
        context_physical_path = self.context.getPhysicalPath()
        if utils.isDefaultPage(self.context, self.request):
            context_physical_path = context_physical_path[:-1]
        context_path = '/'.join(context_physical_path)

        for it in brains:
            brain_path = '/'.join(it.getPath().split('/'))
            is_current = False
            if context_path is not None:
                # Determine if it's current object
                is_current = context_path == it.getPath()
            path_key = '/'.join(it.getPath().split('/')[:-1])
            entry = {
                'id': it.id,
                'uid': it.UID,
                'path': brain_path,
                'url': it.getURL(),
                'title': utils.safe_unicode(it.Title),
                'review_state': it.review_state,
                'is_current': is_current,
                'active_class': is_current and ' c-nav-list__link--active' or ''
            }
            if path_key in ret:
                ret[path_key].append(entry)
            else:
                ret[path_key] = [entry]

        self._nav_tree = ret
        return ret

    def render_item(self, item, path):
        sub = self.build_tree(item['path'], first_run=False)
        if sub:
            item.update({
                'sub': sub,
                'has_sub_class': ' c-nav-list__item--has-subtree'
            })
        else:
            item.update({
                'sub': sub,
                'has_sub_class': '',
            })
        return self._item_markup_template.format(**item)

    def build_tree(self, path, first_run=True):
        """Non-template based recursive tree building.
        3-4 times faster than template based.
        """
        out = u''
        for item in self.nav_tree.get(path, []):
            out += self.render_item(item, path)

        if not first_run and out:
            out = self._subtree_markup_wrapper.format(out=out)
        return out

    def content_tree(self):
        return self.build_tree(
            '/'.join(self.faculty_member().getPhysicalPath())
        )


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
