# -*- coding: UTF-8 -*-
from Acquisition import aq_inner
from five import grok
from hph.lectures.lecture import ILecture
from hph.membership.workspace import IWorkspace
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import form
from z3c.form import button
from zope import schema
from zope.component import getUtility
from zope.lifecycleevent import modified
from zope.schema import getFieldsInOrder

from hph.lectures import MessageFactory as _


class LectureFactory(grok.View):
    grok.context(IWorkspace)
    grok.require('cmf.ModifyPortalContent')
    grok.name('lecture-factory')


class PanelHeadingEditForm(form.SchemaEditForm):
    grok.context(IWorkspace)
    grok.require('cmf.AddPortalContent')
    grok.name('panel-heading')

    schema = ILecture
    ignoreContext = False
    css_class = 'app-form'
    label = _(u"Edit content panel")

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

    def panel(self):
        uid = self.traverse_subpath[2]
        item = api.content.get(UID=uid)
        return item

    @button.buttonAndHandler(_(u"Save"), name="save")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        item = self.panel()
        setattr(item, 'textline', data['textline'])
        modified(item)
        item.reindexObject(idxs='modified')
        api.portal.show_message(_(u"The panel has successfully been updated"),
                                self.request,
                                type='info')
        return self.request.response.redirect(self.next_url())

    @button.buttonAndHandler(_(u"cancel"))
    def handleCancel(self, action):
        msg = _(u"Content panel factory has been cancelled.")
        api.portal.show_message(msg, self.request, type='info')
        return self.request.response.redirect(self.next_url())

    def getContent(self):
        uid = self.traverse_subpath[2]
        item = api.content.get(UID=uid)
        fti = getUtility(IDexterityFTI,
                         name='ade25.panelpage.panel')
        schema = fti.lookupSchema()
        fields = getFieldsInOrder(schema)
        data = {}
        for key, value in fields:
            data[key] = getattr(item, key, value)
        data['textline'] = getattr(item, 'textline', '')
        return data
