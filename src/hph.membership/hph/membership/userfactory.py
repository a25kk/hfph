from five import grok
from plone import api
from Acquisition import aq_inner
from zope import schema
from zope.component import getUtility

from plone.directives import form
from z3c.form import button

from Products.statusmessages.interfaces import IStatusMessage

from hph.membership.tool import IHPHMemberTool
from hph.membership.memberfolder import IMemberFolder

from hph.membership import MessageFactory as _


class IUserCreation(form.Schema):

    email = schema.TextLine(
        title=_(u"E-Mail"),
        required=True,
    )
    fullname = schema.TextLine(
        title=_(u"Fullname"),
        required=True,
    )
    groups = schema.List(
        title=u"Groups",
        value_type=schema.Choice(
            title=u"Group",
            vocabulary="plone.principalsource.Groups"
        ),
        required=False,
    )


class UserCreationForm(form.SchemaEditForm):
    grok.context(IMemberFolder)
    grok.require('cmf.AddPortalContent')
    grok.name('add-new-user')

    schema = IUserCreation
    ignoreContext = True
    css_class = 'app-form'

    label = _(u"Add new user account")

    def updateActions(self):
        super(UserCreationForm, self).updateActions()
        self.actions['save'].addClass("btn btn-primary")
        self.actions['cancel'].addClass("btn btn-link")

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
        tool = getUtility(IHPHMemberTool)
        props = dict(
            fullname=data['fullname'],
        )
        userdata = dict(
            email=data['email'],
            properties=props
        )
        user_id = tool.create_user(userdata)
        for group in data['groups']:
            api.group.add_user(
                groupname=group,
                username=user_id
            )
        IStatusMessage(self.request).addStatusMessage(
            _(u"A new user acount has successfully been created"),
            type='info')
        next_url = context.absolute_url()
        return self.request.response.redirect(next_url)
