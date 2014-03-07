import os

from string import Template
from five import grok
from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot

from hph.membership.memberfolder import IMemberFolder

from hph.membership.mailer import create_plaintext_message
from hph.membership.mailer import prepare_email_message
from hph.membership.mailer import send_email
# send_mail(message, addresses, subject)

from hph.membership import MessageFactory as _


class UserInvitation(grok.View):
    """ Invite specified user to the portal
    """
    grok.context(IMemberFolder)
    grok.require('cmf.ModifyPortalContent')
    grok.name('user-invitation')

    def open_requests(self):
        pwrtool = api.portal.get_tool(name='portal_password_reset')
        return pwrtool.getStats()

    def request_reset(self):
        pwrtool = api.portal.get_tool(name='portal_password_reset')
        user_id = self.request.get('userid', None)
        if user_id:
            open_reset = pwrtool.requestReset(user_id)
            return open_reset

    def build_and_send(self):
        addresses = self.get_addresses()
        subject = _(u"Invitation to join the HfPH relaunch")
        mail_tpl = self._build_mail()
        mail_plain = create_plaintext_message(mail_tpl)
        msg = prepare_email_message(mail_tpl, mail_plain)
        send_email(msg, addresses, subject)
        return 'Done'

    def get_addresses(self):
        recipients = list()
        return recipients

    def _build_mail(self):
        user_id = self.request.get('userid', None)
        template = self._compose_invitation_message(user_id)
        return template

    def _compose_invitation_message(self, user_id):
        user = api.user.get(username=user_id)
        template_file = os.path.join(os.path.dirname(__file__),
                                     'mail-invitation.html')
        template = Template(open(template_file).read())
        template_vars = {
            'id': user_id,
            'email': user.getProperty('email'),
            'fullname': user.getProperty('fullname')
        }
        return template.substitute(template_vars)


class InviteNewMember(grok.View):
    """ Send invitation to new users already added to join and set their
        password and trigger a password reset
    """
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('invite-user')

    def render(self):
        return 'Done sending invitation email'

    def _compose_invitation_message(self):
        template_file = os.path.join(os.path.dirname(__file__),
                                     'mail-invitation.html')
        template = Template(open(template_file).read())
        template_vars = {
            'id': '12345678',
            'email': 'jd@example.tld',
            'fullname': 'John Doe'
        }
        return template.substitute(template_vars)
