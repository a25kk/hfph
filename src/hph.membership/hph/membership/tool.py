import socket
import requests
import contextlib

from five import grok
from plone import api

from zope.component import getUtility
from zope.interface import Interface
from plone.keyring import django_random

from plone.uuid.interfaces import IUUIDGenerator

DEFAULT_SERVICE_URI = 'getAllUsers'
DEFAULT_SERVICE_TIMEOUT = socket.getdefaulttimeout()


class IHPHMemberTool(Interface):
    """ Call processing and optional session data storage entrypoint """

    def create_user(context):
        """ Create plone user records

        The caller is responsible for passing a valid data dictionary
        containing the necessary user details.

        Returns a user id

        @param data:        predefined user data dictionary
        """

    def get(context):
        """ Get user records from external api

        @param timeout:     Set status request timeout
        @param query_type:  Select all or specific user
        @param payload:     Pass additional parameters e.g. user id tokens
        """

    def status(context):
        """ Check availability of external service

        @param timeout: Set status request timeout
        @param query_type:  Select all or specific user
        """


class MemberTool(grok.GlobalUtility):
    grok.provides(IHPHMemberTool)

    def create_user(self, data):
        registration = api.portal.get_tool(name='portal_registration')
        pas = api.portal.get_tool(name='acl_users')
        generator = getUtility(IUUIDGenerator)
        existing = api.user.get(username=data['email'])
        if not existing:
            user_id = generator()
            password = django_random.get_random_string(8)
            roles = ('Member', )
            properties = data['properties']
            properties['workspace'] = user_id
            registration.addMember(
                user_id,
                password,
                roles,
                properties=properties
            )
            pas.updateLoginName(user_id, data['email'])
            user = api.user.get(username=user_id)
        else:
            user = existing
            user_id = user.getId()
        return user_id

    def get(self,
            query_type=DEFAULT_SERVICE_URI,
            **kwargs):
        base_url = self._make_base_query()
        url = '{0}/{1}'.format(base_url, query_type)
        if query_type == DEFAULT_SERVICE_URI:
            with contextlib.closing(requests.get(url)) as response:
                r = response
                if r.status_code == requests.codes.ok:
                    return r.json()
        else:
            with contextlib.closing(requests.get(url)) as response:
                r = response
                if r.status_code == requests.codes.ok:
                    return r.json()

    def status(self,
               query_type=DEFAULT_SERVICE_URI,
               timeout=DEFAULT_SERVICE_TIMEOUT,
               **kwargs):
        info = {}
        base_url = self._make_base_query()
        url = '{0}/{1}'.format(base_url, query_type)
        with contextlib.closing(requests.get(url), timeout=timeout) as response:
            r = response
            sc = r.status_code
            info['code'] = sc
            if sc == requests.codes.ok:
                info['status'] = 'active'
            else:
                info['status'] = 'unreachable'
        return info

    def _make_base_query(self):
        api_uri = self.get_stored_records(token='ip')
        api_key = self.get_stored_records(token='key')
        base_uri = 'http://{0}:8080/{1}/1.0/json/'.format(api_uri, api_key)
        return base_uri

    def get_stored_records(self, token):
        key_base = 'hph.membership.interfaces.IHPHMembershipSettings.api_'
        key = key_base + token
        return api.portal.get_registry_record(key)


def api_group_mapper():
    mapping = {
        'IstGasthoererIn': 'guest',
        'IstDozent': 'lecturer',
        'IstStudent': 'student',
        'IstAlumnus': 'alumni',
        'IstMitgliedProPhilosophia': 'prophil',
    }
    return mapping


def user_group_mapper():
    mapping = {
        'guest': 'Gasthoerer',
        'lecturer': 'Lehrende',
        'student': 'Studierende',
        'alumni': 'Alumni',
        'prophil': 'prophil',
        'media': 'Mediengruppe',
    }
    return mapping
