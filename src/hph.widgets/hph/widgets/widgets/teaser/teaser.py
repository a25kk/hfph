# -*- coding: utf-8 -*-
"""Module providing site widget"""
import uuid as uuid_tool

from plone import api
from plone.app.contenttypes.utils import replace_link_variables_by_paths

import DateTime
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five import BrowserView

from ade25.base.interfaces import IContentInfoProvider
from ade25.panelpage.page import IPage
from ade25.widgets.interfaces import IContentWidgets
from hph.sitecontent.eventitem import IEventItem
from hph.sitecontent.mainsection import IMainSection
from hph.sitecontent.newsentry import INewsEntry


class WidgetTeaserNews(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='teaser-news',
                 widget_type='teaser-news',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
        }
        return self.render()

    def render(self):
        return self.index()

    @property
    def edit_mode(self):
        if self.params['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.params['widget_data']

    def has_content(self):
        if self.widget_content_items():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_content_items(self):
        return self.recent_news()

    def widget_custom_styles(self):
        if self.record and 'styles' in self.record:
            return self.record['styles']
        else:
            return None

    def widget_content_list_class(self):
        context = aq_inner(self.context)
        css_class = 'c-list c-list--gutter c-list--grid c-list--{}'.format(
            context.UID())
        custom_styles = self.widget_custom_styles()
        if custom_styles:
            class_container = custom_styles['class_container']
            for class_name in class_container.split(' '):
                css_class = '{0} c-list--{1}'.format(
                    css_class,
                    class_name
                )
            if 'custom' in custom_styles:
                css_class = '{0} {1}'.format(
                    css_class,
                    custom_styles['custom']
                )
        return css_class

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    def get_latest_news_items(self, limit=3):
        context = aq_inner(self.context)
        items = api.content.find(
            context=context,
            object_provides=INewsEntry.__identifier__,
            review_state='published',
            sort_on='Date',
            sort_order='reverse',
            sort_limit=limit
        )[:limit]
        return items

    def recent_news(self):
        results = []
        brains = self.get_latest_news_items()
        for brain in brains:
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'timestamp': brain.Date,
                'uuid': brain.UID,
                "css_classes": "o-card-list__item--{0}".format(
                    brain.UID
                ),
                'item_object': brain.getObject()
            })
        return results

    @staticmethod
    def widget_more_link():
        portal = api.portal.get()
        more_link = '{0}/nachrichten'.format(portal.absolute_url())
        return more_link


class WidgetTeaserEvents(BrowserView):
    """ Teaser widget for events """

    def __call__(self,
                 widget_name='teaser-events',
                 widget_type='teaser-events',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
        }
        return self.render()

    def render(self):
        return self.index()

    @property
    def edit_mode(self):
        if self.params['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.params['widget_data']

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    def has_content(self):
        if self.widget_has_data():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_data(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        return stored_widget

    @staticmethod
    def widget_display(public):
        if not public and api.user.is_anonymous():
            return False
        return True

    def widget_content(self):
        widget_content = self.widget_data()
        if widget_content:
            data = {
                'title': widget_content.get('title', None),
                'public': widget_content['is_public'],
                'display': self.widget_display(widget_content["is_public"])
            }
        else:
            data = {
                'title': None,
                'public': True,
                'display': True
            }
        return data

    def widget_content_items(self):
        return self.recent_events()

    def widget_custom_styles(self):
        if self.record and 'styles' in self.record:
            return self.record['styles']
        else:
            return None

    def widget_content_list_class(self):
        context = aq_inner(self.context)
        css_class = 'c-list c-list--gutter c-list--grid c-list--{}'.format(
            context.UID())
        custom_styles = self.widget_custom_styles()
        if custom_styles:
            class_container = custom_styles['class_container']
            for class_name in class_container.split(' '):
                css_class = '{0} c-list--{1}'.format(
                    css_class,
                    class_name
                )
            if 'custom' in custom_styles:
                css_class = '{0} {1}'.format(
                    css_class,
                    custom_styles['custom']
                )
        return css_class

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    def widget_has_data(self):
        return len(self.get_latest_event_items()) > 0

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

    def _base_query(self):
        context = aq_inner(self.context)
        date_range_query = {'query': DateTime.DateTime(), 'range': 'min'}
        obj_provides = IEventItem.__identifier__
        return dict(object_provides=obj_provides,
                    path=dict(query='/'.join(context.getPhysicalPath()),
                              depth=1),
                    review_state='published',
                    end=date_range_query,
                    sort_on='start')

    def get_latest_event_items(self, limit=3):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        query = self._base_query()
        query['sort_limit'] = limit
        container = context
        if IPage.providedBy(container):
            container = aq_parent(container)
        acquisition_chain = self._get_acquisition_chain(context)
        for node in acquisition_chain:
            if IMainSection.providedBy(node):
                container = node
        query['path'] = dict(query='/'.join(container.getPhysicalPath()),
                             depth=3)
        if ISiteRoot.providedBy(container):
            query['is_promoted'] = True
        items = catalog.searchResults(query)[:limit]
        return items

    def recent_events(self):
        results = list()
        brains = self.get_latest_event_items()
        for brain in brains:
            results.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
                'timestamp': brain.start,
                'uuid': brain.UID,
                "css_classes": "o-card-list__item--{0}".format(
                    brain.UID
                ),
                'item_object': brain.getObject()
            })
        return results

    def get_link_action(self, link):
        context = aq_inner(self.context)
        link_action = replace_link_variables_by_paths(context, link)
        return link_action

    def widget_more_link(self):
        context = aq_inner(self.context)
        portal = api.portal.get()
        widget_data = self.widget_data()
        if widget_data and widget_data['link']:
            more_link = replace_link_variables_by_paths(
                context, widget_data['link'])
        else:
            more_link = '{0}/@@event-calendar'.format(portal.absolute_url())
        return more_link


class WidgetTeaserLinksInternal(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='teaser-links-internal',
                 widget_type='teaser-links-internal',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
        }
        return self.render()

    def render(self):
        return self.index()

    @property
    def edit_mode(self):
        if self.params['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.params['widget_data']

    def has_content(self):
        if self.widget_content_items():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_data(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        return stored_widget

    @staticmethod
    def widget_display(public):
        if not public and api.user.is_anonymous():
            return False
        return True

    def widget_content(self):
        widget_content = self.widget_data()
        if widget_content:
            data = {
                'title': widget_content.get('title', None),
                'public': widget_content.get('is_public', None),
                'display': self.widget_display(
                    widget_content.get('is_public', None)
                )
            }
        else:
            data = {
                'title': None,
                'public': True,
                'display': True
            }
        return data

    def widget_item_nodes(self):
        context = aq_inner(self.context)
        ordered_nodes = list()
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        if stored_widget:
            ordered_nodes = stored_widget["item_order"]
        return ordered_nodes

    def has_widget_item_nodes(self):
        return len(self.widget_item_nodes()) > 0

    def widget_item_content(self, widget_node):
        context = aq_inner(self.context)
        item_content = {
            "uid": widget_node
        }
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        if stored_widget:
            content_items = stored_widget["items"]
            if content_items:
                try:
                    item_content.update(content_items[widget_node])
                except KeyError:
                    item_content = None
        return item_content

    def get_link_action(self, link):
        context = aq_inner(self.context)
        link_action = replace_link_variables_by_paths(context, link)
        return link_action

    def widget_content_items(self):
        return self.widget_item_nodes()

    def widget_custom_styles(self):
        if self.record and 'styles' in self.record:
            return self.record['styles']
        else:
            return None

    def widget_content_list_class(self):
        context = aq_inner(self.context)
        css_class = 'c-list c-list--gutter c-list--grid c-list--{}'.format(
            context.UID())
        custom_styles = self.widget_custom_styles()
        if custom_styles:
            class_container = custom_styles['class_container']
            for class_name in class_container.split(' '):
                css_class = '{0} c-list--{1}'.format(
                    css_class,
                    class_name
                )
            if 'custom' in custom_styles:
                css_class = '{0} {1}'.format(
                    css_class,
                    custom_styles['custom']
                )
        return css_class

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp


class WidgetTeaserLinksExternal(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='teaser-links-external',
                 widget_type='teaser-links-external',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
        }
        return self.render()

    def render(self):
        return self.index()

    @property
    def edit_mode(self):
        if self.params['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.params['widget_data']

    def has_content(self):
        if self.widget_content_items():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_data(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        return stored_widget

    @staticmethod
    def widget_display(public):
        if not public and api.user.is_anonymous():
            return False
        return True

    def widget_content(self):
        widget_content = self.widget_data()
        if widget_content:
            is_public = widget_content.get('is_public', None)
            data = {
                'title': widget_content.get('title', None),
                'public': is_public,
                'display': self.widget_display(is_public)
            }
        else:
            data = {
                'title': None,
                'public': True,
                'display': True
            }
        return data

    def widget_item_nodes(self):
        context = aq_inner(self.context)
        ordered_nodes = list()
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        if stored_widget:
            ordered_nodes = stored_widget["item_order"]
        return ordered_nodes

    def has_widget_item_nodes(self):
        return len(self.widget_item_nodes()) > 0

    def widget_item_content(self, widget_node):
        context = aq_inner(self.context)
        item_content = {
            "uid": widget_node
        }
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.widget_uid()
        )
        if stored_widget:
            content_items = stored_widget["items"]
            if content_items:
                try:
                    item_content.update(content_items[widget_node])
                except KeyError:
                    item_content = None
        return item_content

    def get_link_action(self, link):
        context = aq_inner(self.context)
        link_action = replace_link_variables_by_paths(context, link)
        return link_action

    def widget_content_items(self):
        return self.widget_item_nodes()

    def widget_custom_styles(self):
        if self.record and 'styles' in self.record:
            return self.record['styles']
        else:
            return None

    def widget_content_list_class(self):
        context = aq_inner(self.context)
        css_class = 'c-list c-list--gutter c-list--grid c-list--{}'.format(
            context.UID())
        custom_styles = self.widget_custom_styles()
        if custom_styles:
            class_container = custom_styles['class_container']
            for class_name in class_container.split(' '):
                css_class = '{0} c-list--{1}'.format(
                    css_class,
                    class_name
                )
            if 'custom' in custom_styles:
                css_class = '{0} {1}'.format(
                    css_class,
                    custom_styles['custom']
                )
        return css_class

    @staticmethod
    def time_stamp(item, date_time):
        content_info_provider = IContentInfoProvider(item)
        time_stamp = content_info_provider.time_stamp(date_time)
        return time_stamp

    @staticmethod
    def has_stored_image(image_object):
        context = image_object
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def image_tag(self, image_uid):
        image = api.content.get(UID=image_uid)
        if self.has_stored_image(image):
            figure = image.restrictedTraverse('@@figure')(
                image_field_name='image',
                caption_field_name='image_caption',
                scale='ratio-4:3',
                aspect_ratio='4/3',
                lqip=True,
                lazy_load=True
            )
            return figure
        return None
