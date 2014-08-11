# -*- coding: UTF-8 -*-
"""Module to allow contributions on lecture content"""

from Acquisition import aq_inner
from five import grok
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import form
from z3c.form import button
from zope.component import getUtility
from zope.lifecycleevent import modified
from zope.schema import getFieldsInOrder

from hph.lectures.lecture import ILecture
from hph.lectures.coursedetails import ICourseDetails
from hph.lectures.coursemodules import ICourseModuleInformation
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


class LectureBaseEditForm(form.SchemaEditForm):
    grok.context(IWorkspace)
    grok.require('cmf.AddPortalContent')
    grok.name('lecture-base')

    schema = ILecture
    ignoreContext = True
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

    def next_url(self):
        context = aq_inner(self.context)
        row = self.traverse_subpath[0]
        url = '{0}/@@panelblock-editor/{1}'.format(
            context.absolute_url(), row)
        return url

    def content_item(self):
        uid = self.traverse_subpath[2]
        item = api.content.get(UID=uid)
        return item

    @button.buttonAndHandler(_(u"Save"), name="save")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        item = self.content_item()
        setattr(item, 'textline', data['textline'])
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
        fti = getUtility(IDexterityFTI,
                         name='ade25.panelpage.panel')
        schema = fti.lookupSchema()
        fields = getFieldsInOrder(schema)
        data = {}
        for key, value in fields:
            data[key] = getattr(item, key, value)
        return data
