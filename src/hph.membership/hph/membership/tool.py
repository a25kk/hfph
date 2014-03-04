import socket
import requests
import contextlib
import smtplib
from five import grok
from plone import api
from zope.interface import Interface

DEFAULT_SERVICE_URI = 'getAllUsers'
DEFAULT_SERVICE_TIMEOUT = socket.getdefaulttimeout()


class IHPHMemberTool(Interface):
    """ Call processing and optional session data storage entrypoint """

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
        params = kwargs.iteritems()
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
        'media': 'Mediangruppe',
    }
    return mapping
