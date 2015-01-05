# -*- coding: UTF-8 -*-
"""Module to allow contributions on lecture content"""

import json
import datetime
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from five import grok
from plone import api
from plone.directives import form
from z3c.form import button
from zope.component import getMultiAdapter
from zope.lifecycleevent import modified
from zope.schema import getFieldsInOrder

from hph.lectures.interfaces import ILectureBase
from hph.membership.workspace import IWorkspace

from hph.lectures import MessageFactory as _


class LectureFactory(grok.View):
    grok.context(IWorkspace)
    grok.require('cmf.ModifyPortalContent')
    grok.name('lecture-factory')

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def content_item(self):
        uid = self.traverse_subpath[0]
        item = api.content.get(UID=uid)
        return item


class LectureBaseEditForm(form.SchemaEditForm):
    grok.context(IWorkspace)
    grok.require('cmf.AddPortalContent')
    grok.name('lecture-base')

    schema = ILectureBase
    ignoreContext = False
    css_class = 'app-form'
    label = _(u"Edit course base information")

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def content_item(self):
        uid = self.traverse_subpath[0]
        item = api.content.get(UID=uid)
        return item

    def next_url(self):
        context = aq_inner(self.context)
        item = self.traverse_subpath[0]
        url = '{0}/@@lecture-factory/{1}'.format(
            context.absolute_url(), item)
        return url

    @button.buttonAndHandler(_(u"Save"), name="save")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        item = self.content_item()
        schema = ILectureBase
        fields = getFieldsInOrder(schema)
        for key, value in fields:
            try:
                new_value = data[key]
                setattr(item, key, new_value)
            except KeyError:
                continue
        modified(item)
        item.reindexObject(idxs='modified')
        api.portal.show_message(_(u"The item has successfully been updated"),
                                self.request,
                                type='info')
        return self.request.response.redirect(self.next_url())

    @button.buttonAndHandler(_(u"cancel"))
    def handleCancel(self, action):
        msg = _(u"Content item factory has been cancelled.")
        api.portal.show_message(msg, self.request, type='info')
        return self.request.response.redirect(self.next_url())

    def getContent(self):
        item = self.content_item()
        schema = ILectureBase
        fields = getFieldsInOrder(schema)
        data = {}
        for key, value in fields:
            data[key] = getattr(item, key, value)
        return data


class LectureEditor(grok.View):
    grok.context(IWorkspace)
    grok.require('cmf.ModifyPortalContent')
    grok.name('lecture-editor')

    def update(self):
        context = aq_inner(self.context)
        self.errors = {}
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('field-name')
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            errorIdx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {}
                        error['active'] = True
                        error['msg'] = _(u"This field is required")
                        form_errors[value] = error
                        errorIdx += 1
                    else:
                        error = {}
                        error['active'] = False
                        error['msg'] = form[value]
                        form_errors[value] = error
            if errorIdx > 0:
                self.errors = form_errors
            else:
                self._store_data(form)

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def content_item(self):
        uid = self.traverse_subpath[0]
        item = api.content.get(UID=uid)
        return item

    def next_url(self):
        context = aq_inner(self.context)
        item = self.traverse_subpath[0]
        url = '{0}/@@lecture-factory/{1}'.format(
            context.absolute_url(), item)
        return url

    def getFieldname(self):
        return self.traverse_subpath[1]

    def getFieldData(self):
        context = self.content_item()
        fieldname = self.traverse_subpath[1]
        return getattr(context, fieldname, '')

    def _store_data(self, data):
        item = self.content_item()
        fieldname = self.getFieldname()
        new_value = data['content-editable-form-body']
        setattr(item, fieldname, new_value)
        modified(item)
        item.reindexObject(idxs='modified')
        api.portal.show_message(_(u"The item has successfully been updated"),
                                self.request,
                                type='info')
        return self.request.response.redirect(self.next_url())


class LectureEditorSaveData(grok.View):
    grok.context(IWorkspace)
    grok.require('cmf.ModifyPortalContent')
    grok.name('lecture-editor-save')

    def render(self):
        form = self.request.form
        timestamp = datetime.datetime.now()
        msg = _(u"Serialized data stored successful.")
        results = {
            'success': True,
            'message': msg,
            'timestamp': timestamp
        }
        self.request.response.setHeader('Content-Type',
                                        'application/json; charset=utf-8')
        return json.dumps(results)
