# -*- coding: utf-8 -*-
"""Module providing catalog query based nav trees"""
from Products.CMFPlone.interfaces import INavigationSchema
from plone.app.layout.navigation.root import getNavigationRoot
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.contentprovider.provider import ContentProviderBase


class NavTreeProvider(ContentProviderBase):

    _navtree = None
    _navtree_path = None
    _navtree_context = None

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INavigationSchema, prefix='plone')
        return settings

    @property
    def navtree_path(self):
        if self._navtree_path is None:
            self._navtree_path = getNavigationRoot(self.context)
        return self._navtree_path

    @property
    def navtree_depth(self):
        return self.settings.navigation_depth

    @property
    def enableDesc(self):
        return True

    @property
    def navtree(self):

        if self._navtree is not None:
            return self._navtree

        types = plone.api.portal.get_registry_record('plone.displayed_types')
        lang_current = plone.api.portal.get_current_language()

        query = {
            'path': {'query': self.navtree_path, 'depth': self.navtree_depth},
            'portal_type': {'query': types},
            'exclude_from_nav': False,
            'Language': lang_current,
            'sort_on': 'getObjPositionInParent',
        }
        res = plone.api.content.find(**query)

        ret = {}
        for it in res:
            pathkey = '/'.join(it.getPath().split('/')[:-1])
            entry = {
                'id': it.id,
                'uid': it.UID,
                'url': it.getURL(),
                'title': it.Title,
                'review_state': it.review_state,
            }
            if pathkey in ret:
                ret[pathkey].append(entry)
            else:
                ret[pathkey] = [entry]

        self._navtree = ret
        return ret

    def build_tree(self, path, first_run=True):
        """Non-template based recursive tree building.
        3-4 times faster than template based.
        See figures below.
        """
        normalizer = getUtility(IIDNormalizer)
        out = u''
        for it in self.navtree.get(path, []):
            sub = self.build_tree(path + '/' + it['id'], first_run=False)
            opener = u"""<input id="navitem-{uid}" type="checkbox" class="opener">
                         </input><label for="navitem-{uid}"></label>""".format(
                uid=it['uid']
            ) if sub else ''
            out += u'<li class="{id}{has_sub_class}">'.format(
                id=normalizer.normalize(it['id']),
                has_sub_class=' has_subtree' if sub else '',
            )
            out += u'<a href="{url}" class="state-{review_state}">{title}</a>{opener}'.format(  # noqa
                url=it['url'],
                review_state=it['review_state'],
                title=it['title'],
                opener=opener if sub else ''
            )
            out += sub
            out += u'</li>'

        if not first_run:
            out = u'<ul class="has_subtree dropdown">' + out + u'</ul>' if out else ''
        return out

    def render(self):

        return self.build_tree(self.navtree_path)
