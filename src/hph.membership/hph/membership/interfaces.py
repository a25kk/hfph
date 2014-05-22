from zope import schema
from zope.interface import Interface

from hph.membership import MessageFactory as _


class IHPHMembershipTool(Interface):
    """ A marker inteface for a specific theme layer """


class IHPHMembershipSettings(Interface):
    """ API secrets, tokens and keys stored in the registry """

    api_ip = schema.TextLine(
        title=_(u"MembershipTool IP")
    )
    api_version = schema.TextLine(
        title=_(u"MembershipTool API Version")
    )
    api_key = schema.TextLine(
        title=_(u"MembershipTool API Key"),
    )
    api_token = schema.TextLine(
        title=_(u"Membership Tool API Token"),
        description=_(u"This API token can be used to authenticate with the "
                      u"portal e.g. when calling the member updater via "
                      u"external cronjob"),
    )
