# -*- coding: utf-8 -*-
"""Module providing site widget"""
import uuid as uuid_tool

from Acquisition import aq_inner
from Products.Five import BrowserView
from ade25.base.interfaces import IContentInfoProvider
from hph.sitecontent.eventitem import IEventItem
from hph.sitecontent.newsentry import INewsEntry
from plone import api


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

    @staticmethod
    def get_latest_news_items(limit=3):
        portal = api.portal.get()
        items = api.content.find(
            context=portal,
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
    def get_latest_event_items(limit=3):
        portal = api.portal.get()
        items = api.content.find(
            context=portal,
            object_provides=IEventItem.__identifier__,
            review_state='published',
            sort_on='Start',
            sort_order='reverse',
            sort_limit=limit
        )[:limit]
        return items

    def recent_events(self):
        results = []
        brains = self.get_latest_event_items()
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

    def recent_news(self):
        results = []
        elements = [
            #'8303a7b4b3ad460f93f23db372f5f2d1',
            #'c5fd0c9ccb484de2aa689d94545e6f20',
            #'9a5c757860f24e5a9985c35fd9c11590',
            #'533766a3059940828c0da7ffce1cc755'
        ]
        for item_uid in elements:
            brain = api.content.get(UID=item_uid)
            results.append({
                'title': brain.Title(),
                'description': brain.Description(),
                'url': brain.absolute_url(),
                'timestamp': brain.Date(),
                'uuid': brain.UID(),
                "css_classes": "o-card-list__item--{0}".format(
                    brain.UID()
                ),
                'item_object': brain
            })
        return results

    @staticmethod
    def widget_more_link():
        portal = api.portal.get()
        more_link = '{0}/nachrichten'.format(portal.absolute_url())
        return more_link
