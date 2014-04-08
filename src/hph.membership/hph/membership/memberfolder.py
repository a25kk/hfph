import datetime
import json
from Acquisition import aq_inner
from five import grok
from plone import api
from zope import schema
from zope.component import getUtility
from zope.lifecycleevent import modified

from plone.directives import form
from plone.dexterity.content import Container
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.memoize.view import memoize

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone.utils import safe_unicode

from hph.membership.tool import api_group_mapper
from hph.membership.tool import user_group_mapper
from hph.membership.tool import IHPHMemberTool

from hph.membership import MessageFactory as _


class IMemberFolder(form.Schema, IImageScaleTraversable):
    """
    Container for member workspaces
    """
    importable = schema.TextLine(
        title=_(u"Importable API Records"),
        required=False,
    )


class MemberFolder(Container):
    grok.implements(IMemberFolder)
    pass


class View(grok.View):
    grok.context(IMemberFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.available = self.has_view_permission()
        self.is_anon = api.user.is_anonymous()

    def render(self):
        if self.available:
            return self.request.response.redirect(self.usermanager_url())
        else:
            return self.request.response.redirect(self.workspace_url())

    def workspace_url(self):
        context = aq_inner(self.context)
        here_url = context.absolute_url()
        user = api.user.get_current()
        userid = user.getId()
        if userid in context.keys():
            url = '{0}/{1}'.format(here_url, userid)
        else:
            url = '{0}/@@workspace-missing'.format(here_url)
        return url

    def usermanager_url(self):
        context = aq_inner(self.context)
        here_url = context.absolute_url()
        url = '{0}/@@user-manager'.format(here_url)
        return url

    def has_view_permission(self):
        context = aq_inner(self.context)
        admin_roles = ('Manager', 'Site Administrator', 'StaffMember')
        is_adm = False
        if not api.user.is_anonymous():
            user = api.user.get_current()
            userid = user.getId()
            if userid is 'zope-admin':
                is_adm = True
            roles = api.user.get_roles(username=userid, obj=context)
            for role in roles:
                if role in admin_roles:
                    is_adm = True
        return is_adm


class WorkspaceMissing(grok.View):
    grok.context(IMemberFolder)
    grok.require('zope2.View')
    grok.name('workspace-missing')


class UserManager(grok.View):
    grok.context(IMemberFolder)
    grok.require('cmf.ModifyPortalContent')
    grok.name('user-manager')

    def update(self):
        self.has_users = len(self.get_all_members()) > 0

    @property
    def traverse_subpath(self):
        return self.subpath

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def has_workspace(self, userid):
        context = aq_inner(self.context)
        if userid in context.keys():
            return True
        return False

    @memoize
    def get_all_members(self):
        users = []
        records = api.user.get_users()
        for record in records:
            data = {}
            user = api.user.get(username=record.getId())
            userid = user.getId()
            email = user.getProperty('email')
            groups = api.group.get_groups(username=userid)
            user_groups = list()
            for group in groups:
                gid = group.getId()
                if gid != 'AuthenticatedUsers':
                    user_groups.append(gid)
            data['userid'] = userid
            data['email'] = email
            data['name'] = user.getProperty('fullname', userid)
            data['enabled'] = user.getProperty('enabled')
            data['confirmed'] = user.getProperty('confirmed')
            data['groups'] = user_groups
            data['workspace'] = user.getProperty('workspace')
            users.append(data)
        return users

    def records_idx(self):
        return len(self.userrecords())

    def records_timestamp(self):
        data = self.stored_data()
        return data['timestamp']

    def usergroups(self):
        groups = api.group.get_groups()
        return groups

    def stored_data(self):
        context = aq_inner(self.context)
        stored_data = getattr(context, 'importable', None)
        data = json.loads(stored_data)
        return data

    def userdata(self):
        data = self.stored_data()
        return data['items']

    def userrecords(self):
        records = []
        if self.userdata() is not None:
            for item in self.userdata():
                userid = item['EMail']
                group_list = self.construct_group_list(item)
                if userid and len(group_list) > 0:
                    user = {}
                    user['id'] = item['ID']
                    user['email'] = userid.lower()
                    user['fullname'] = item['VollerName']
                    user['groups'] = group_list
                    records.append(user)
        return records

    def construct_group_list(self, item):
        api_mapper = api_group_mapper()
        group_mapper = user_group_mapper()
        groups = list()
        for key in api_mapper.keys():
            stored_value = item[key]
            if stored_value is True:
                api_groupname = api_mapper[key]
                groupname = group_mapper[api_groupname]
                groups.append(groupname)
        return groups


class MemberRecords(grok.View):
    grok.context(IMemberFolder)
    grok.require('cmf.ManagePortal')
    grok.name('member-records')


class StoredRecords(grok.View):
    grok.context(IMemberFolder)
    grok.require('cmf.ManagePortal')
    grok.name('stored-member-records')

    def render(self):
        return json.dumps(self.preprocess_data())

    def preprocess_data(self):
        data = {
            "iTotalRecords": len(self.userdata()),
            "iTotalDisplayRecords": "10",
            "sEcho": "10",
            "aaData": self.userrecords()
        }
        return data

    def stored_data(self):
        context = aq_inner(self.context)
        stored_data = getattr(context, 'importable', None)
        data = json.loads(stored_data)
        return data

    def userdata(self):
        data = self.stored_data()
        return data['items']

    def userrecords(self):
        records = []
        if self.userdata() is not None:
            for item in self.userdata():
                userid = item['EMail']
                email = userid.lower()
                group_list = self.construct_group_list(item)
                if userid and len(group_list) > 0:
                    user = {}
                    user['id'] = item['ID']
                    user['email'] = email
                    user['fullname'] = safe_unicode(item['VollerName'])
                    user['groups'] = group_list
                    records.append(user)
        return records

    def construct_group_list(self, item):
        api_mapper = api_group_mapper()
        group_mapper = user_group_mapper()
        groups = list()
        for key in api_mapper.keys():
            stored_value = item[key]
            if stored_value is True:
                api_groupname = api_mapper[key]
                groupname = group_mapper[api_groupname]
                groups.append(groupname)
        return groups


class UpdateRecords(grok.View):
    grok.context(IMemberFolder)
    grok.require('cmf.ManagePortal')
    grok.name('update-member-records')

    def render(self):
        new_records = self.get_importable_records()
        IStatusMessage(self.request).addStatusMessage(
            _(u"External records stored for import"),
            type='info')
        here_url = self.context.absolute_url()
        next_url = '{0}/@@user-manager?imported_records={1}'.format(
            here_url, len(new_records))
        return self.request.response.redirect(next_url)

    def get_importable_records(self):
        context = aq_inner(self.context)
        tool = getUtility(IHPHMemberTool)
        records = tool.get_external_users()
        timestamp = datetime.datetime.now()
        data = {
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'items': records['APIData']
        }
        import_data = json.dumps(data)
        setattr(context, 'importable', import_data)
        modified(context)
        context.reindexObject(idxs='modified')
        return records


class CreateRecords(grok.View):
    grok.context(IMemberFolder)
    grok.require('cmf.ManagePortal')
    grok.name('create-member-records')

    def render(self):
        created = self.create_records()
        msg = 'Created {0} new member records'.format(created)
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        next_url = self.context.absolute_url()
        return self.request.response.redirect(next_url)

    def create_records(self):
        records = self.userrecords()
        tool = getUtility(IHPHMemberTool)
        idx = 0
        imported = 0
        for record in records:
            idx += 1
            props = dict(
                fullname=safe_unicode(record['fullname']),
                record_id=str(record['id']),
            )
            data = dict(
                email=record['email'],
                properties=props
            )
            user_info = tool.create_user(data)
            user_id = user_info['userid']
            is_new_user = user_info['created']
            if is_new_user is True:
                for group in record['groups']:
                    api.group.add_user(
                        groupname=group,
                        username=user_id
                    )
                tool.invite_user(user_id)
                imported += 1
        return imported

    def userdata(self):
        context = aq_inner(self.context)
        stored_data = getattr(context, 'importable', None)
        import_data = json.loads(stored_data)
        data = import_data['items']
        return data

    def userrecords(self):
        records = []
        if self.userdata() is not None:
            for item in self.userdata():
                userid = item['EMail']
                email = userid.lower()
                group_list = self.construct_group_list(item)
                if userid and len(group_list) > 0:
                    user = {}
                    user['id'] = item['ID']
                    user['email'] = email
                    user['fullname'] = safe_unicode(item['VollerName'])
                    user['groups'] = group_list
                    records.append(user)
        return records

    def construct_group_list(self, item):
        api_mapper = api_group_mapper()
        group_mapper = user_group_mapper()
        groups = list()
        for key in api_mapper.keys():
            stored_value = item[key]
            if stored_value is True:
                api_groupname = api_mapper[key]
                groupname = group_mapper[api_groupname]
                groups.append(groupname)
        return groups
