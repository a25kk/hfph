import json
from five import grok
from plone import api
from Acquisition import aq_inner
from zope.interface import Interface
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.layout.navigation.navtree import NavtreeStrategyBase
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy

from plone.app.layout.viewlets.interfaces import IPortalFooter

from hph.sitecontent.contentpage import IContentPage


class NavbarView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('navbar-view')

    def update(self):
        pstate = getMultiAdapter((self.context, self.request),
                                 name='plone_portal_state')
        self.portal_url = pstate.portal_url
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()

        self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']
        self.selected_section = self.selected_tabs['portal']

    def render_json(self):
        return json.dumps(self.site_nav())

    def selectedTabs(self, default_tab='index_html', portal_tabs=()):
        plone_url = api.portal.get().absolute_url()
        plone_url_len = len(plone_url)
        request = self.request
        valid_actions = []
        url = request['URL']
        path = url[plone_url_len:]
        for action in portal_tabs:
            if not action['url'].startswith(plone_url):
                continue
            action_path = action['url'][plone_url_len:]
            if not action_path.startswith('/'):
                action_path = '/' + action_path
            if path.startswith(action_path + '/') or path == action_path:
                valid_actions.append((len(action_path), action['id']))
        valid_actions.sort()
        if valid_actions:
            return {'portal': valid_actions[-1][1]}
        return {'portal': default_tab}

    def site_nav(self):
        navtree = self.siteNavStrategy()
        return navtree

    def siteNavStrategy(self):
        context = aq_inner(self.context)
        selected_tab = self.selected_portal_tab
        obj = api.portal.get()[selected_tab]
        path = {'query': '/'.join(obj.getPhysicalPath()),
                'navtree': 1,
                'navtree_start': 2,
                'depth': 2}
        query = {
            'path': path,
            'review_state': 'published',
            'portal_type': ('hph.sitecontent.mainsection',
                            'hph.sitecontent.contentpage',
                            'hph.lectures.coursefolder')
        }
        strategy = SitemapNavtreeStrategy(obj)
        strategy.rootPath = '/'.join(obj.getPhysicalPath())
        strategy.showAllParents = True
        strategy.bottomLevel = 999
        tree = buildFolderTree(context, obj, query, strategy)
        items = []
        for c in tree['children']:
            item = {}
            item['item'] = c['item']
            item['children'] = c.get('children', '')
            item['itemid'] = c['normalized_id']
            item_id = c['normalized_id']
            if item_id == context.getId():
                item['class'] = 'active'
            else:
                item['class'] = ''
            item['parent'] = self.compute_parent_marker(item_id)
            items.append(item)
        return items

    def compute_parent_marker(self, item_id):
        context = aq_inner(self.context)
        path_ids = context.getPhysicalPath()
        marker = False
        if item_id in path_ids:
            marker = True
        return marker


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
        self.has_subsubsections = len(self.get_subsubsections()) > 0
        #self.selected_tabs = self.selectedItems(
        #    portal_tabs=self.main_sections())
        portal_tabs_view = getMultiAdapter((self.context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()

        self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']
        self.selected_section = self.selected_tabs['portal']

    def selectedTabs(self, default_tab='index_html', portal_tabs=()):
        plone_url = getToolByName(self.context, 'portal_url')()
        plone_url_len = len(plone_url)
        request = self.request
        valid_actions = []
        url = request['URL']
        path = url[plone_url_len:]
        for action in portal_tabs:
            if not action['url'].startswith(plone_url):
                continue
            action_path = action['url'][plone_url_len:]
            if not action_path.startswith('/'):
                action_path = '/' + action_path
            if path.startswith(action_path + '/') or path == action_path:
                valid_actions.append((len(action_path), action['id']))
        valid_actions.sort()
        if valid_actions:
            return {'portal': valid_actions[-1][1]}
        return {'portal': default_tab}

    def site_nav(self):
        navtree = self.siteNavStrategy()
        return navtree

    def siteNavStrategy(self):
        context = aq_inner(self.context)
        root = getNavigationRoot(context)
        selected_tab = self.selected_portal_tab
        obj = api.portal.get()[selected_tab]
        path = {'query': '/'.join(obj.getPhysicalPath()),
                'navtree': 1,
                'navtree_start': 1,
                'depth': 3}
        query = {
            'path': path,
            'review_state': 'published',
            'portal_type': ('hph.sitecontent.mainsection',
                            'hph.sitecontent.contentpage',
                            'hph.lectures.coursefolder'),
            'sort_order': 'getObjPositionInParent'
        }
        root_obj = context.unrestrictedTraverse(root)
        strategy = DefaultNavtreeStrategy(root_obj)
        strategy.rootPath = '/'.join(root_obj.getPhysicalPath())
        strategy.showAllParents = False
        strategy.bottomLevel = 999
        tree = buildFolderTree(query)
        items = []
        for c in tree['children']:
            item = {}
            item['item'] = c['item']
            item['children'] = c.get('children', '')
            item_id = c['item'].getId
            if item_id == context.getId():
                item['class'] = 'active'
            else:
                item['class'] = ''
            item['itemid'] = item_id
            items.append(item)
        return tree

    def show_sectionname(self):
        display = False
        if self.selected_section and self.selected_section != 'index_html':
            display = True
        return display

    def prettify_section_name(self, name):
        portal = api.portal.get()
        tab = self.selected_section
        pretty_title = ''
        if tab != 'index_html':
            section = portal[name]
            pretty_title = section.pretty_title_or_id()
        return pretty_title

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

    def get_subsubsections(self):
        context = aq_inner(self.context)
        types = ('hph.sitecontent.contentpage', 'hph.lectures.coursefolder')
        depth = 3
        navtree = self.navStrategy(context, types, depth)
        return navtree

    def sub_sections(self, obj=None):
        pstate = getMultiAdapter((self.context, self.request),
                                 name='plone_portal_state')
        if obj is not None:
            root_obj = obj
        else:
            root_obj = pstate.portal()
        types = ('hph.sitecontent.contentpage',
                 'hph.publications.publicationfolder',
                 'hph.lectures.coursefolder',
                 'hph.faculty.facultydirectory')
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
            item['current'] = c['currentItem']
            item['is_parent'] = c['currentParent']
            item_id = c['item'].getId
            item['itemid'] = item_id
            item['marker'] = self.compute_navitem_marker(item_id)
            items.append(item)
        return items

    def compute_navitem_marker(self, item_id):
        context = aq_inner(self.context)
        path_ids = context.getPhysicalPath()
        marker = False
        if item_id == context.getId():
            marker = True
        if item_id in path_ids:
            marker = True
        return marker

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
