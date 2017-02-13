# -*- coding: utf-8 -*-
"""Module providing user management and search"""
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PasswordResetTool import django_random
from hph.membership import MessageFactory as _
from plone import api
# from plone.app.users.browser.membersearch import extractCriteriaFromRequest
from z3c.form import button
from z3c.form import form
from plone.autoform.form import AutoExtensibleForm
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxWidget
from zope.component import getMultiAdapter
from zope import schema
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


class IUserSearchSchema(model.Schema):
    """Provide schema for member search."""

    model.fieldset(
        'extra',
        label=_(u'legend_member_search_criteria',
                default=u'User Search Criteria'),
        fields=['login', 'email', 'fullname']
    )

    login = schema.TextLine(
        title=_(u'label_name', default=u'Name'),
        description=_(
            u'help_search_name',
            default=u'Find users whose login name contain'),
        required=False,
    )
    email = schema.TextLine(
        title=_(u'label_email', default=u'E-mail'),
        description=_(
            u'help_search_email',
            default=u'Find users whose email address contain'),
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
            'groups': user_groups
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

    def member_record_details(self, user_data):
        data = {}
        try:
            user_id = user_data.getId()
        except AttributeError:
            import pdb; pdb.set_trace()
            pass
        user = api.user.get(username=user_data.getId())
        email = user.getProperty('email')
        groups = api.group.get_groups(username=user_id)
        user_groups = list()
        for group in groups:
            gid = group.getId()
            if gid != 'AuthenticatedUsers':
                user_groups.append(gid)
        data['user_id'] = user_id
        data['email'] = email
        data['name'] = user.getProperty('fullname', user_id)
        data['enabled'] = user.getProperty('enabled')
        data['confirmed'] = user.getProperty('confirmed')
        data['groups'] = user_groups
        data['workspace'] = user.getProperty('workspace')
        return data


@implementer(IPublishTraverse)
class UserDetails(BrowserView):
    """Manage user details"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def user_info(self):
        context = aq_inner(self.context)
        info = {}
        userid = self.subpath[0]
        user = api.user.get(username=userid)
        info['fullname'] = user.getProperty('fullname', '') or userid
        info['email'] = user.getProperty('email', _(u"No email provided"))
        info['login_time'] = user.getProperty('last_login_time', '')
        info['enabled'] = user.getProperty('enabled', '')
        info['confirmed'] = user.getProperty('confirmed', '')
        info['worklist'] = user.getProperty('worklist', list())
        return info

    def get_user_details(self):
        context = aq_inner(self.context)
        user_id = self.subpath[0]
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

    def compose_pwreset_link(self):
        context = aq_inner(self.context)
        user_id = self.subpath[0]
        user = api.user.get(username=user_id)
        token = self._access_token(user)
        portal_url = api.portal.get().absolute_url()
        url = '{0}/useraccount/{1}/{2}'.format(
            portal_url, user_id, token)
        return url

    def _access_token(self, user):
        stored_token = user.getProperty('token', '')
        if len(stored_token):
            token = stored_token
        else:
            token = django_random.get_random_string(length=12)
            user.setMemberProperties(mapping={'token': token})
        return token


class UserManager(BrowserView):
    """ Manage portal members """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self):
        return self.index()

    def __call__(self):
        self.results = None
        self.submitted = False
        self.errors = dict()
        return self.render()

    def update(self):
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('title', )
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            error_idx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {
                            'active': True,
                            'msg': _(u"This field is required")
                        }
                        form_errors[value] = error
                        error_idx += 1
                    else:
                        error = {
                            'active': True,
                            'msg': form[value]
                        }
                        form_errors[value] = error
            if error_idx > 0:
                self.errors = form_errors
            else:
                self._search_records(form)

    def member_records(self):
        return None

    def _search_records(self, data):
        context = aq_inner(self.context)
        view = context.restrictedTraverse('@@pas_search')
        criteria = extractCriteriaFromRequest(self.request.form.copy())
        self.results = view.searchUsers(sort_by=u'fullname', **criteria)
        return self.results
