# -*- coding: utf-8 -*-
"""Module providing an json data storage api"""
import datetime
import json
import time
import uuid as uuid_tool
from Products.CMFPlone.utils import safe_unicode
from plone import api
from plone.memoize.view import memoize
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
        stored = getattr(item, 'moduleInformation', dict())
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
            stored = data
        end = time.time()
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
        return records

    def safe_encode(self, value):
        """Return safe unicode version of value.
        """
        su = safe_unicode(value)
        return su.encode('utf-8')
