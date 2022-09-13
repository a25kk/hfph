# -*- coding: UTF-8 -*-
from plone.dexterity.content import Container
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model

from zope import schema
from zope.interface import implementer

from hph.membership import MessageFactory as _



class IMemberFolder(model.Schema, IImageScaleTraversable):
    """
    Container for member workspaces
    """
    importable = schema.TextLine(
        title=_(u"Importable API Records"),
        required=False,
    )


@implementer(IMemberFolder)
class MemberFolder(Container):
    pass
