# -*- coding: utf-8 -*-
"""Module providing user management and search"""
from AccessControl import Unauthorized
from Acquisition import aq_inner
from hph.membership import MessageFactory as _
from hph.membership.tool import IHPHMemberTool
from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.protect.utils import addTokenToUrl
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PasswordResetTool import django_random
from z3c.form import button
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxWidget
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


class IUserSearchSchema(model.Schema):
    """Provide schema for member search."""

    model.fieldset(
        'extra',
        label=_(u'legend_member_search_criteria',
                default=u'User Search Criteria'),
        fields=['login', 'fullname']
    )

    login = schema.TextLine(
        title=_(u'label_name', default=u'Name'),
        description=_(
            u'help_search_name',
            default=u'Find users whose login name contain'),
        required=False,
    )
    fullname = schema.TextLine(
        title=_(u'label_fullname', default=u'Full Name'),
        description=_(
            u'help_search_fullname',
            default=u'Find users whose full names contain'),
        required=False,
    )
    model.fieldset(
        'groups',
        label=_(u'legend_member_search_groups',
                default=u'User Group Search'),
        fields=['groups']
    )
    directives.widget('groups', CheckBoxWidget)
    groups = schema.List(
        title=_(u'label_groups', default=u'Group(s)'),
        description=_(
            u'help_search_groups',
            default=u'Find all members of selected groups.'),
        required=False,
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.Groups',
        ),
    )


def extractCriteriaFromRequest(criteria):
    """Takes a dictionary of z3c.form data and sanitizes it to fit
    for a pas member search.
    """
    for key in ['_authenticator',
                'form.buttons.search',
                'form.widgets.groups-empty-marker', ]:
        if key in criteria:
            del criteria[key]
    for (key, value) in criteria.items():
        if not value:
            del criteria[key]
        else:
            new_key = key.replace('form.widgets.', '')
            criteria[new_key] = value
            del criteria[key]

    return criteria


class UserSearchForm(AutoExtensibleForm, form.Form):
    """This search form enables you to find users by specifying one or more
    search criteria.
    """

    schema = IUserSearchSchema
    ignoreContext = True

    label = _(u'heading_member_search', default=u'Search for users')
    description = _(u'description_member_search',
                    default=u'This search form enables you to find users by '
                            u'specifying one or more search criteria.')
    template = ViewPageTemplateFile('usermanager.pt')
    enableCSRFProtection = True
    formErrorsMessage = _('There were errors.')

    submitted = False

    def can_manage_users(self):
        """ Check for user management permissions """
        context = aq_inner(self.context)
        tool = getUtility(IHPHMemberTool)
        can_manage_users = tool.can_manage_users(context)
        return can_manage_users

    def has_workspace(self, user_id):
        context = aq_inner(self.context)
        if user_id in context.keys():
            return True
        return False

    def _get_user_details(self, user_id, user):
        context = aq_inner(self.context)
        has_workspace = False
        if self.has_workspace(user_id):
            has_workspace = True
        groups = api.group.get_groups(username=user_id)
        user_groups = list()
        for group in groups:
            gid = group.getId()
            if gid != 'AuthenticatedUsers':
                user_groups.append(gid)
        details_url = '{0}/@@user-management-details?user-id={1}'.format(
            context.absolute_url(), user_id
        )
        user_details_url = addTokenToUrl(details_url)
        user_info = {
            'email': user.getProperty('email'),
            'user_id': user_id,
            'name': user.getProperty('fullname', user.getId()),
            'enabled': user.getProperty('enabled'),
            'confirmed': user.getProperty('confirmed'),
            'has_workspace': has_workspace,
            'workspace': user.getProperty('workspace'),
            'workspace_url': '{}/{}'.format(
                context.absolute_url(),
                user.getProperty('workspace')
            ),
            'groups': user_groups,
            'details_link': user_details_url
        }
        return user_info

    def _clean_user_data(self, user_data):
        records = list()
        for user in user_data:
            try:
                user_id = user.getId()
            except AttributeError:
                user_id = user['userid']
            user_object = api.user.get(username=user_id)
            user_details = self._get_user_details(user_id, user_object)
            records.append(user_details)
        return records

    @staticmethod
    def merge_search_results(cleaned, original):
        output = {}
        for entry in cleaned:
            key = entry['user_id']
            if key not in output:
                if any(d['userid'] == key for d in original):
                    # does already exist
                    output[key] = entry.copy()
            else:
                buf = entry.copy()
                buf.update(output[key])
                output[key] = buf
        return output.values()

    @button.buttonAndHandler(_(u'label_search', default=u'Search'),
                             name='search')
    def handleApply(self, action):
        request = self.request
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        if request.get('form.buttons.search', None):
            self.submitted = True
            view = self.context.restrictedTraverse('@@pas_search')
            criteria = extractCriteriaFromRequest(self.request.form.copy())
            results_user = view.searchUsers(sort_by=u'fullname', **criteria)
            # Keep original search result for later merge reference
            # by using a copy for further processing
            results = results_user[:]
            if 'groups' in criteria:
                for group in criteria['groups']:
                    for record in api.user.get_users(groupname=group):
                        results.append(record)
            cleaned_results = self._clean_user_data(results)
            # Remove potential duplicates using the pas merge method
            search_results = view.merge(cleaned_results, 'user_id')
            if results_user:
                user_records = self.merge_search_results(
                    search_results,
                    results_user)
            else:
                user_records = search_results
            self.results = user_records


@implementer(IPublishTraverse)
class UserDetails(BrowserView):
    """Manage user details"""

    def can_manage_users(self):
        """ Check for user management permissions """
        context = aq_inner(self.context)
        tool = getUtility(IHPHMemberTool)
        can_manage_users = tool.can_manage_users(context)
        return can_manage_users

    def get_user_object(self):
        user_id = self.request.get('user-id', None)
        user = api.user.get(username=user_id)
        return user

    def get_user_details(self):
        context = aq_inner(self.context)
        # user_token = self.subpath[0]
        # user_id = user_token.replace('user-id-', '')
        user_id = self.request.get('user-id', None)
        user = api.user.get(username=user_id)
        groups = api.group.get_groups(username=user_id)
        user_groups = list()
        for group in groups:
            gid = group.getId()
            if gid != 'AuthenticatedUsers':
                user_groups.append(gid)
        user_info = {
            'fullname': user.getProperty('fullname', '') or user_id,
            'email': user.getProperty('email'),
            'user_id': user_id,
            'name': user.getProperty('fullname', user.getId()),
            'enabled': user.getProperty('enabled'),
            'confirmed': user.getProperty('confirmed'),
            'login_time': user.getProperty('last_login_time', ''),
            'workspace': user.getProperty('workspace'),
            'workspace_url': '{}/{}'.format(
                context.absolute_url(),
                user.getProperty('workspace')
            ),
            'worklist': user.getProperty('worklist', list()),
            'groups': user_groups
        }
        return user_info

    @staticmethod
    def protect_url(url):
        return addTokenToUrl(url)

    def compose_pwreset_link(self):
        user = self.get_user_object()
        token = self._access_token(user)
        portal_url = api.portal.get().absolute_url()
        url = '{0}/useraccount/{1}/{2}'.format(
            portal_url, user.getId(), token)
        return url

    def _access_token(self, user):
        stored_token = user.getProperty('token', '')
        if len(stored_token):
            token = stored_token
        else:
            token = django_random.get_random_string(length=12)
            user.setMemberProperties(mapping={'token': token})
        return token


class UserEnable(BrowserView):
    """ Enable user account """

    def __call__(self):
        return self.render()

    def render(self):
        context = aq_inner(self.context)
        authenticator = getMultiAdapter((context, self.request),
                                        name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized
        user_id = self.request.get('user-id', None)
        tool = getUtility(IHPHMemberTool)
        if tool.can_manage_users(context):
            tool.update_user(user_id, {
                'enabled': True
            })
        base_url = '{0}/@@user-manager-details?user-id={1}'.format(
            context.absolute_url(),
            user_id
        )
        next_url = '{0}&_authenticator={1}'.format(
            base_url,
            authenticator.token()
        )
        api.portal.show_message(
            message=_(u"User account enabled."),
            request=self.request)
        return self.request.response.redirect(next_url)


class UserDisable(BrowserView):
    """ Disable user account """

    def __call__(self):
        return self.render()

    def render(self):
        context = aq_inner(self.context)
        authenticator = getMultiAdapter((context, self.request),
                                        name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized
        user_id = self.request.get('user-id', None)
        tool = getUtility(IHPHMemberTool)
        if tool.can_manage_users(context):
            tool.update_user(user_id, {
                'enabled': False
            })
        base_url = '{0}/@@user-manager-details?user-id={1}'.format(
            context.absolute_url(),
            user_id
        )
        next_url = '{0}&_authenticator={1}'.format(
            base_url,
            authenticator.token()
        )
        api.portal.show_message(
            message=_(u"User was successfully disabled."),
            request=self.request)
        return self.request.response.redirect(next_url)


class UserRemove(BrowserView):
    """ Disable user account """

    def __call__(self):
        return self.render()

    def render(self):
        context = aq_inner(self.context)
        authenticator = getMultiAdapter((context, self.request),
                                        name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized
        user_id = self.request.get('user-id', None)
        tool = getUtility(IHPHMemberTool)
        if tool.can_manage_users(context):
            tool.remove_user(user_id)
        base_url = '{0}/@@user-management'.format(context.absolute_url())
        next_url = '{0}?_authenticator={1}'.format(
            base_url,
            authenticator.token()
        )
        api.portal.show_message(
            message=_(u"User account successfully removed form portal"),
            request=self.request)
        return self.request.response.redirect(next_url)

