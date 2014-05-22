import datetime
import json
import time
from five import grok
from plone import api
from zope.component import getUtility
from zope.lifecycleevent import modified
from Products.CMFPlone.utils import safe_unicode

from plone.app.layout.navigation.interfaces import INavigationRoot

from hph.membership.tool import api_group_mapper
from hph.membership.tool import user_group_mapper
from hph.membership.tool import IHPHMemberTool


class MemberRecords(grok.View):
    """ Create plone user records from external data

        The caller is responsible for passing a valid token maching a
        predefined value in @@hph-membershiptool-settings.

        Construct an URI like this:
        http://localhost:8404/hph/member-record-updater/{action}/{token}

        Returns a status message

        @param action:       Desired action: update or create
        @param token:        predefined api token
    """
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('member-record-updater')

    def render(self):
        status = self._process_update()
        msg = 'Member Records: {0}'.format(status)
        return msg

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []
        self.subpath.append(name)
        return self

    def is_equal(self, a, b):
        """ Constant time comparison """
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
        return result == 0

    def get_access_token(self):
        key = 'hph.membership.interfaces.IHPHMembershipSettings.api_token'
        return api.portal.get_registry_record(key)

    def has_valid_token(self):
        token = self.subpath[1]
        stored_token = self.get_access_token()
        if stored_token is None:
            return False
        return self.is_equal(stored_token, token)

    def memberfolder(self):
        portal = api.portal.get()
        return portal['ws']

    def userdata(self):
        context = self.memberfolder()
        stored_data = getattr(context, 'importable', None)
        import_data = json.loads(stored_data)
        data = import_data['items']
        return data

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

    def _process_api_update(self):
        context = self.memberfolder()
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
        idx = len(records['APIData'])
        process_state = '{0} user records imported'.format(idx)
        return process_state

    def _process_user_import(self):
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
        process_state = '{0} user accounts created'.format(imported)
        return process_state

    def _process_update(self):
        process_state = 'Puhuhu: aborted due to some unknown error...'
        start_time = time.time()
        if self.has_valid_token():
            request_type = self.subpath[0]
            if request_type == 'update':
                process_state = self._process_api_update()
            elif request_type == 'create':
                process_state = self._process_user_import()
        processing_time = time.time() - start_time
        return '{0} in {1} seconds'.format(process_state, processing_time)
