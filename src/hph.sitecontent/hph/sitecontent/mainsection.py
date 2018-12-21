# -*- coding: utf-8 -*-
"""Module providing section container content type"""
from Acquisition import aq_inner
from five import grok
from plone.app.z3cform.widget import LinkFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implementer

from hph.sitecontent import MessageFactory as _


class IMainSection(model.Schema, IImageScaleTraversable):
    """
    Folder to represent the site sections
    """
    image = NamedBlobImage(
        title=_(u"Banner image"),
        required=False,
    )

    model.fieldset(
        'redirect',
        label=u"Redirect",
        fields=['link', ]
    )

    directives.widget(link=LinkFieldWidget)
    link = schema.TextLine(
        title=_(u"Link"),
        description=_(u"Optional internal or external link that will be "
                      u"used as redirection target when section is accessed."
                      u"Logged in users will see the target link instead."),
        required=False,
    )


@implementer(IMainSection)
class MainSection(Container):

    def canSetDefaultPage(self):
        return False



class View(grok.View):
    grok.context(IMainSection)
    grok.require('zope2.View')
    grok.name('view')

    def banner_image(self):
        obj = aq_inner(self.context)
        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('image', width=870, height=421)
        data = {}
        if scale is not None:
            data['url'] = scale.url
            data['width'] = scale.width
            data['height'] = scale.height
        return data
