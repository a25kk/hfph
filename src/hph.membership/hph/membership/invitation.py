import os

from string import Template
from five import grok
from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot

from hph.membership.memberfolder import IMemberFolder


class UserInvitation(grok.View):
    """ Invite specified user to the portal
    """
    grok.context(IMemberFolder)
    grok.require('cms.ModifyPortalContent')
    grok.name('user-invitation')

    def open_requests(self):
        pwrtool = api.portal.get_tool(name='portal_passwordreset')
        return pwrtool.getStats()

    def request_reset(self):
        pwrtool = api.portal.get_tool(name='portal_passwordreset')
        user_id = self.request.get('user_id', None)
        if user_id:
            open_reset = pwrtool.requestReset(user_id)
            return open_reset


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
