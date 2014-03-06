import os

from string import Template
from five import grok
from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot


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
                                     'invitationmail.tpl')
        template = Template(open(template_file).read())

        template_vars = {
            'id': self.id(),
            'options': self._getOptions()
        }

        return template.substitute(template_vars)
