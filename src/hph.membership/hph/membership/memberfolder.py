from Acquisition import aq_inner
from five import grok
from plone import api
from zope import schema
from zope.component import getUtility
from zope.lifecycleevent import modified

from plone.directives import form
from plone.dexterity.content import Container
from plone.namedfile.interfaces import IImageScaleTraversable
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
        self.has_users = len(self.get_all_members()) > 0

    def get_all_members(self):
        users = []
        records = api.user.get_users()
        for record in records:
            data = {}
            user = api.user.get(username=record.getId())
            data['userid'] = user.getId()
            data['email'] = user.getProperty('email')
            users.append(data)
        return users

    def records_idx(self):
        return len(self.userrecords())

    def usergroups(self):
        groups = api.group.get_groups()
        return groups

    def userdata(self):
        context = aq_inner(self.context)
        import_data = getattr(context, 'importable', None)
        data = import_data['APIData']
        return data

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
        next_url = '{0}?imported_records={1}'.format(here_url, len(new_records))
        return self.request.response.redirect(next_url)

    def get_importable_records(self):
        context = aq_inner(self.context)
        tool = getUtility(IHPHMemberTool)
        records = tool.get()
        setattr(context, 'importable', records)
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
        idx = 0
        imported = 0
        for record in records[5:10]:
            idx += 1
            new_id = uuid_userid_generator(record)
            user_email = (record['email']).lower()
            existing = api.user.get(username=user_email)
            if not existing:
                user = api.user.create(
                    username=new_id,
                    email=user_email.lower(),
                )
            else:
                user = existing
            member_properties = dict(
                fullname=safe_unicode(record['fullname']),
                record_id=str(record['id'])
            )
            member = api.user.get(username=user.getId())
            if member:
                member.setMemberProperties(mapping=member_properties)
            imported += 1
            for group in record['groups']:
                api.group.add_user(
                    groupname=group,
                    username=user.getId()
                )
        return imported

    def userdata(self):
        context = aq_inner(self.context)
        import_data = getattr(context, 'importable', None)
        data = import_data['APIData']
        return data

    def userrecords(self):
        records = []
        if self.userdata() is not None:
            for item in self.userdata():
                userid = item['EMail']
                group_list = self.construct_group_list(item)
                if userid and len(group_list) > 0:
                    user = {}
                    user['id'] = item['ID']
                    user['email'] = userid
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
