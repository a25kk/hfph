from five import grok
from Acquisition import aq_inner
from zope.interface import Interface
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.layout.navigation.navtree import NavtreeStrategyBase
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy

from plone.app.layout.viewlets.interfaces import IPortalFooter

from hph.sitecontent.contentpage import IContentPage


class NavbarViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalFooter)
    grok.name('hph.sitecontent.NavbarViewlet')

    def update(self):
        pstate = getMultiAdapter((self.context, self.request),
                                 name='plone_portal_state')
        self.portal_url = pstate.portal_url
        self.available = len(self.subsections()) > 0
        self.has_subsections = len(self.get_subsections()) > 0
        self.selected_tabs = self.selectedItems(
            portal_tabs=self.main_sections())
        self.selected_section = self.selected_tabs['portal']

    def main_sections(self):
        sections = self.sections()
        results = []
        for section in sections:
            item = section['item']
            data = {'name': item.Title,
                    'id': item.getId,
                    'url': item.getURL(),
                    'description': item.Description}
            results.append(data)
        return results

    def subsections(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IContentPage.__identifier__,
                          review_state='published',
                          sort_on='getObjPositionInParent',
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1))
        return results

    def isActiveItem(self, itemid):
        context = aq_inner(self.context)
        context_id = context.getId()
        if itemid == context_id:
            return 'navitem active'
        else:
            return 'navitem'

    def sections(self):
        pstate = getMultiAdapter((self.context, self.request),
                                 name='plone_portal_state')
        portal = pstate.portal()
        types = ('hph.sitecontent.mainsection',)
        depth = 1
        navtree = self.navStrategy(portal, types, depth)
        return navtree

    def get_subsections(self):
        context = aq_inner(self.context)
        sections = self.sections()
        subsections = {}
        for section in sections:
            section_brain = section['item']
            section_id = section_brain.getId
            if section_id == context.getId():
                subsections = self.sub_sections(context)
            else:
                subsections = self.sub_sections(context)
        return subsections

    def sub_sections(self, obj=None):
        pstate = getMultiAdapter((self.context, self.request),
                                 name='plone_portal_state')
        if obj is not None:
            root_obj = obj
        else:
            root_obj = pstate.portal()
        types = ('hph.sitecontent.contentpage',
                 'hph.publications.publicationfolder')
        depth = 2
        navtree = self.navStrategy(root_obj, types, depth)
        return navtree

    def navStrategy(self, obj, types, start):
        context = aq_inner(self.context)
        root = getNavigationRoot(context)
        path = {'query': '/'.join(obj.getPhysicalPath()),
                'navtree': 1,
                'navtree_start': start}
        query = {
            'path': path,
            'review_state': 'published',
            'portal_type': types,
            'sort_order': 'getObjPositionInParent'
        }
        root_obj = context.unrestrictedTraverse(root)
        strategy = DefaultNavtreeStrategy(root_obj)
        strategy.rootPath = '/'.join(root_obj.getPhysicalPath())
        strategy.showAllParents = False
        strategy.topLevel = 2
        strategy.bottomLevel = 999
        tree = buildFolderTree(root_obj, root_obj,
                               query, strategy=NavtreeStrategyBase())
        items = []
        for c in tree['children']:
            item = {}
            item['item'] = c['item']
            item['children'] = c.get('children', '')
            items.append(item)
        return items

    def selectedItems(self, default_tab='index_html', portal_tabs=()):
        plone_url = getToolByName(self.context, 'portal_url')()
        plone_url_len = len(plone_url)
        request = self.request
        valid_actions = []

        url = request['URL']
        path = url[plone_url_len:]

        for action in portal_tabs:
            if not action['url'].startswith(plone_url):
                # In this case the action url is an external link. Then, we
                # avoid issues (bad portal_tab selection) continuing with next
                # action.
                continue
            action_path = action['url'][plone_url_len:]
            if not action_path.startswith('/'):
                action_path = '/' + action_path
            if path.startswith(action_path + '/') or path == action_path:
                # Make a list of the action ids, along with the path length
                # for choosing the longest (most relevant) path.
                valid_actions.append((len(action_path), action['id']))

        # Sort by path length, the longest matching path wins
        valid_actions.sort()
        if valid_actions:
            return {'portal': valid_actions[-1][1]}

        return {'portal': default_tab}
