# -*- coding: utf-8 -*-
"""Module providing catalog query based nav trees"""
from Products.CMFPlone.utils import safe_unicode
from hph.sitecontent.browser.controlpanel import IHphBaseControlPanelNavigation
from plone import api
from plone.app.layout.navigation.root import getNavigationRoot
from plone.i18n.normalizer import IIDNormalizer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.contentprovider.provider import ContentProviderBase


class NavTreeProvider(ContentProviderBase):

    _nav_tree = None
    _nav_tree_path = None
    _nav_tree_context = None

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IHphBaseControlPanelNavigation,
            prefix='hph.base')
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
            'exclude_from_nav': False,
            'Language': lang_current,
            'sort_on': 'getObjPositionInParent',
        }
        res = api.content.find(**query)

        ret = {}
        for it in res:
            path_key = '/'.join(it.getPath().split('/')[:-1])
            entry = {
                'id': it.id,
                'uid': it.UID,
                'url': it.getURL(),
                'title': it.Title,
                'review_state': it.review_state,
            }
            if path_key in ret:
                ret[path_key].append(entry)
            else:
                ret[path_key] = [entry]

        self._nav_tree = ret
        return ret

    def build_tree(self, path, first_run=True, iteration=0):
        """Non-template based recursive tree building.
        3-4 times faster than template based.
        See figures below.
        """
        normalizer = getUtility(IIDNormalizer)
        out = u''
        for it in self.nav_tree.get(path, []):
            sub = self.build_tree(path + '/' + it['id'],
                                  first_run=False,
                                  iteration=iteration+1)
            opener = u"""<input id="navitem-{uid}" type="checkbox" class="opener">
                         </input><label for="navitem-{uid}"></label>""".format(
                uid=it['uid']
            ) if sub else ''
            out += u'<li class="c-nav__item c-nav__item--{id}{has_sub_class}">'.format(
                id=normalizer.normalize(it['id']),
                has_sub_class=' c-nav__item--has-children' if sub else '',
            )
            out += u'<a href="{url}" class="c-nav__link c-nav__link--state-{review_state}">{title}</a>{opener}'.format(  # noqa
                url=it['url'],
                review_state=it['review_state'],
                title=safe_unicode(it['title']),
                opener=opener if sub else ''
            )
            out += sub
            out += u'</li>'

        if not first_run:
            base_list = u'<ul class="c-nav c-nav--level-1 c-nav--level-{0} has_subtree dropdown">'.format(
                iteration
            )
            out = base_list + out + u'</ul>' if out else ''
        return out

    def render(self):

        return self.build_tree(self.nav_tree_path)
