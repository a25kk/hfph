import socket
import requests
import contextlib

from DateTime import DateTime
from five import grok
from plone import api

from zope.component import getUtility
from zope.interface import Interface
from plone.keyring import django_random

from plone.uuid.interfaces import IUUIDGenerator

from hph.membership.mailer import create_plaintext_message
from hph.membership.mailer import prepare_email_message
from hph.membership.mailer import get_mail_template
from hph.membership.mailer import send_mail

DEFAULT_SERVICE_URI = 'getAllUsers'
DEFAULT_SERVICE_TIMEOUT = socket.getdefaulttimeout()

from hph.membership import MessageFactory as _


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

    def start_password_reset(context):
        """ Trigger password reset process for a specific user records

        @param uid:         unique user_id
        """


class MemberTool(grok.GlobalUtility):
    grok.provides(IHPHMemberTool)

    def create_user(self, data):
        registration = api.portal.get_tool(name='portal_registration')
        pas = api.portal.get_tool(name='acl_users')
        # portal = api.portal.get()
        # request = getattr(portal, "REQUEST", None)
        generator = getUtility(IUUIDGenerator)
        existing = api.user.get(username=data['email'])
        if not existing:
            user_id = generator()
            user_email = data['email']
            password = django_random.get_random_string(8)
            properties = data['properties']
            properties['workspace'] = user_id
            properties['email'] = user_email
            properties['creation_time'] = DateTime()
            registration.addMember(
                user_id,
                password
                # REQUEST=request
            )
            pas.updateLoginName(user_id, user_email)
            user = api.user.get(username=user_id)
            user.setMemberProperties(mapping=properties)
        else:
            user = existing
            user_id = user.getId()
        return user_id

    def get_user(self, user_id):
        return api.user.get(username=user_id)

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
        with contextlib.closing(requests.get(url), timeout=timeout) as resp:
            r = resp
            sc = r.status_code
            info['code'] = sc
            if sc == requests.codes.ok:
                info['status'] = 'active'
            else:
                info['status'] = 'unreachable'
        return info

    def start_password_reset(self, userid):
        user = self.get_user(userid)
        subject = _(u"Einladung zur neuen hfph.de Seite")
        mail_tpl = self._compose_invitation_message(userid)
        mail_plain = create_plaintext_message(mail_tpl)
        msg = prepare_email_message(mail_tpl, mail_plain)
        recipients = list()
        recipients.append(user.getProperty('email'))
        send_mail(msg, recipients, subject)
        return userid

    def _compose_invitation_message(self, user_id, message_type):
        user = self.get_user(user_id)
        token = self._access_token(user)
        portal_url = api.portal.get().absolute_url()
        url = '{0}/useraccount/{1}/{2}'.format(
            portal_url, user_id, token)
        template_vars = {
            'id': user_id,
            'email': user.getProperty('email'),
            'fullname': user.getProperty('fullname'),
            'url': url
        }
        template_name = 'mail-{}'.format(message_type)
        message = get_mail_template(template_name, template_vars)
        return message

    def _access_token(self, user):
        new_token = django_random.get_random_string(length=12)
        stored_token = user.getProperty('token', '')
        if len(stored_token):
            token = stored_token
        else:
            token = new_token
        return token

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
