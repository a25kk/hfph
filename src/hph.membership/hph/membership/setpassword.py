from Acquisition import aq_inner
from five import grok
from hph.membership import MessageFactory as _
from plone import api
from plone.directives import form
from z3c.form import button
from zope import schema
from zope.publisher.interfaces import IPublishTraverse

from Products.CMFPlone.PasswordResetTool import InvalidRequestError, \
    ExpiredRequestError
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.layout.navigation.interfaces import INavigationRoot


class IUserPassword(form.Schema):

    password = schema.TextLine(
        title=_(u"New Password"),
        required=True,
    )
    confirm = schema.TextLine(
        title=_(u"Again for confirmation"),
        required=True,
    )


class SetUserPassword(form.SchemaForm):
    grok.context(INavigationRoot)
    grok.implements(IPublishTraverse)
    grok.require('zope2.View')
    grok.name('set-user-password')

    schema = IUserPassword
    ignoreContext = True
    css_class = 'app-form'

    label = _(u"Add new password")

    def update(self):
        self.request.set('disable_border', True)
        self.key = self.traverse_subpath[0]
        super(SetUserPassword, self).update()

    def updateActions(self):
        super(SetUserPassword, self).updateActions()
        self.actions['save'].addClass("btn btn-primary")
        self.actions['cancel'].addClass("btn btn-link")

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    @button.buttonAndHandler(_(u"Add new user"), name="save")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)

    @button.buttonAndHandler(_(u"cancel"))
    def handleCancel(self, action):
        context = aq_inner(self.context)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Process has been cancelled."),
            type='info')
        return self.request.response.redirect(context.absolute_url())

    def applyChanges(self, data):
        context = aq_inner(self.context)
        pwtool = api.portal.get_tool(name='portal_password_reset')
        try:
            pwtool.verifyKey(self.key)
        except InvalidRequestError:
            IStatusMessage(self.request).addStatusMessage(
                _(u"This password request reset is invalid"),
                type='info')
        except ExpiredRequestError:
            IStatusMessage(self.request).addStatusMessage(
                _(u"This password request reset is invalid"),
                type='info')
        IStatusMessage(self.request).addStatusMessage(
            _(u"A new password has been set"),
            type='info')
        next_url = context.absolute_url()
        return self.request.response.redirect(next_url)
