# -*- coding: utf-8 -*-
"""Module providing catalog query based nav trees"""
from collections import defaultdict

from Products.CMFPlone import utils
from Products.CMFPlone.interfaces import ILanguageSchema
from hph.sitecontent.browser.controlpanel import IHphBaseControlPanelNavigation
from plone import api
from plone.app.layout.navigation.root import getNavigationRoot
from plone.i18n.normalizer import IIDNormalizer
from plone.memoize.view import memoize_contextless
from plone.registry.interfaces import IRegistry
from zope.component import getUtility, getMultiAdapter
from zope.contentprovider.provider import ContentProviderBase

from hph.sitecontent import config as hph_config


class SitemapProvider(ContentProviderBase):

    _nav_tree = None
    _nav_tree_path = None
    _nav_tree_context = None

    _opener_markup_template = (
        u'<span class="c-toc__link-item c-toc__link-item--icon">'  # noqa: E 501
        u'<svg class="o-icon o-icon--default o-icon--circle o-icon__ui--add-dims c-toc__icon c-toc__icon--open"><use xlink:href="/assets/symbol/svg/sprite.symbol.svg#ui--add"></use></svg>'  # noqa: E 501
        u'<svg class="o-icon o-icon--default o-icon--circle o-icon__ui--remove-dims c-toc__icon c-toc__icon--close"><use xlink:href="/assets/symbol/svg/sprite.symbol.svg#ui--remove"></use></svg>'  # noqa: E 501
        u'</span>'
    )
    _item_markup_template = (
        u'<li class="c-toc__item {id}{has_sub_class}">'
        u'<a href="{url}" class="c-toc__link state-{review_state}{js_class}"{aria_haspopup}><span class="c-toc__link-item">{title}</span>{opener}</a>'  # noqa: E 501
        u'{sub}'
        u'</li>'
    )
    _subtree_markup_wrapper = (
        u'<ul class="c-toc c-toc--level-1 o-toc__subtree o-menu o-menu--toc o-menu--hidden js-collapsible-item">{out}</ul>'  # noqa: E 501
    )

    @property
    @memoize_contextless
    def settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IHphBaseControlPanelNavigation,
            prefix='hph.base')
        return settings

    @property
    def language_settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILanguageSchema, prefix='plone')
        return settings

    @property
    def nav_tree_path(self):
        if self._nav_tree_path is None:
            self._nav_tree_path = getNavigationRoot(self.context)
        return self._nav_tree_path

    @property
    def nav_tree_depth(self):
        try:
            navigation_depth = self.settings.navigation_depth
        except AttributeError:
            navigation_depth = 3
        return navigation_depth

    @property
    def nav_tree_element_open(self):
        try:
            navigation_element = self.settings.navigation_element_open
        except AttributeError:
            navigation_element = hph_config.navigation_elements(action='open')
        return navigation_element

    @property
    def enableDesc(self):
        return True

    @property
    def nav_tree(self):

        if self._nav_tree is not None:
            return self._nav_tree

        types = api.portal.get_registry_record(
            name='hph.base.listed_content_types'
        )
        lang_current = api.portal.get_current_language()

        query = {
            'path': {'query': self.nav_tree_path, 'depth': self.nav_tree_depth},
            'portal_type': {'query': types},
            'exclude_from_toc': False,
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
                'is_current': is_current
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
                'opener':  self._opener_markup_template.format(**item),
                'aria_haspopup': ' aria-haspopup="true"',
                'has_sub_class': ' c-toc__item--has-subtree',
                'js_class': ' js-collapsible-toggle'
            })
        else:
            item.update({
                'sub': sub,
                'opener':  '',
                'aria_haspopup': '',
                'has_sub_class': '',
                'js_class': ''
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

    def render(self):
        return self.build_tree(self.nav_tree_path)
