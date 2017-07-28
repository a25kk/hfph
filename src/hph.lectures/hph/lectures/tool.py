# -*- coding: utf-8 -*-
"""Module providing an json data storage api"""
import datetime
import json
import time
import uuid as uuid_tool
from Products.CMFPlone.utils import safe_unicode
from collective.beaker.interfaces import ISession
from plone import api
from plone.memoize.view import memoize
from zope.globalrequest import getRequest
from zope.lifecycleevent import modified


class CourseModuleTool(object):
    """ Factory providing CRUD operations for course module management """

    def create(self, uuid, data=None):
        item = api.content.get(UID=uuid)
        start = time.time()
        initial_data = self._create_record(uuid, item, data)
        end = time.time()
        initial_data.update(dict(_runtime=str(end-start)))
        json_data = json.dumps(initial_data)
        setattr(item, 'moduleInformation', json_data)
        modified(item)
        item.reindexObject(idxs='modified')
        return json_data

    # @memoize
    def read(self, uuid, key=None):
        item = api.content.get(UID=uuid)
        stored = getattr(item, 'moduleInformation', None)
        data = dict()
        if stored is not None:
            data = json.loads(stored)
        if key is not None:
            records = data['items']
            data = records[int(key)]
        return data

    def update(self, uuid, data, key=None):
        stored = self.read(uuid)
        start = time.time()
        if key is not None:
            records = stored['items']
            records[key] = data
        else:
            records = data
        end = time.time()
        stored['items'] = records
        stored.update(dict(_runtime=str(end-start),
                           timestamp=str(int(time.time())),
                           updated=str(datetime.datetime.now())))
        updated = json.dumps(stored)
        item = api.content.get(UID=uuid)
        setattr(item, 'moduleInformation', updated)
        modified(item)
        item.reindexObject(idxs='modified')
        return uuid

    def delete(self, uuid, key=None):
        stored = self.read(uuid)
        if key is not None:
            stored[key] = dict()
            updated = json.dumps(stored)
            item = api.content.get(UID=uuid)
            setattr(item, 'moduleInformation', updated)
            modified(item)
            item.reindexObject(idxs='modified')
        return uuid

    def _create_record(self, uuid, item, data):
        records = {
            "id": str(uuid_tool.uuid4()),
            "uid": str(uuid),
            "timestamp": str(int(time.time())),
            "_runtime": "0.0000059604644775390625",
            "created": datetime.datetime.now().isoformat(),
            "title": item.Title(),
            "items": []
        }
        # Add potential initial data
        if data:
            records['items'].append(data)
        return records

    def safe_encode(self, value):
        """Return safe unicode version of value.
        """
        su = safe_unicode(value)
        return su.encode('utf-8')


class CourseFilterTool(object):
    """ Module filter session storage tool

        Store selected filter configuration inside anonymous session
        to provide dynamically constructed filter forms
    """

    @staticmethod
    def get(key=None):
        """ Create module filter session """
        portal = api.portal.get()
        session_id = 'hph.lectures.filter.{0}'.format(
            '.'.join(portal.getPhysicalPath())
        )
        if key:
            session_id = 'hph.lectures.filter.{0}'.format(key)
        session = ISession(getRequest())
        if session_id not in session:
            session[session_id] = dict()
            session.save()
        return session[session_id]

    @staticmethod
    def destroy(key=None):
        """ Destroy module filter session """
        portal = api.portal.get()
        session_id = 'hph.lectures.filter.{0}'.format(
            '.'.join(portal.getPhysicalPath())
        )
        if key:
            session_id = 'hph.lectures.filter.{0}'.format(key)
        session = ISession(getRequest())
        if session_id in session:
            del session[session_id]
            session.save()

    def add(self, key, data=None):
        """
            Add item to survey session
        """
        survey = self.get()
        item = self.update(key, data)
        if not item:
            survey[key] = data
            return survey[key]

    def update(self, key, data):
        survey = self.get()
        item_id = key
        if item_id in survey:
            survey[item_id] = data
            return survey[item_id]
        return None

    def remove(self, key):
        survey = self.get()
        if key in survey:
            del survey[key]
            return key

    @staticmethod
    def create_record(token, data):
        records = {
            "id": str(uuid_tool.uuid4()),
            "timestamp": str(int(time.time())),
            "_runtime": "0.00000000000000000001",
            "created": datetime.datetime.now().isoformat(),
            "token": token,
            "filter": []
        }
        # Add potential initial data
        if data:
            records['filter'].append(data)
        return records


class CourseFilterUpdater(object):
    """ Factory providing CRUD operations for course module filters """
    @staticmethod
    def _create_record(data):
        records = {
            "id": str(uuid_tool.uuid4()),
            "timestamp": str(int(time.time())),
            "_runtime": "0.00000000000000000001",
            "created": datetime.datetime.now().isoformat(),
            "filter": []
        }
        # Add potential initial data
        if data:
            records['filter'].append(data)
        return records
