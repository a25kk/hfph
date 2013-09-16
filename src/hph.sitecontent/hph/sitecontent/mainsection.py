from Acquisition import aq_inner
from five import grok
from plone.directives import dexterity, form
from zope.component import getMultiAdapter

from zope import schema

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText

from hph.sitecontent import MessageFactory as _


class IMainSection(form.Schema, IImageScaleTraversable):
    """
    Forder to represent the main site sections
    """
    image = NamedBlobImage(
        title=_(u"Banner image"),
        required=False,
    )


class MainSection(dexterity.Container):
    grok.implements(IMainSection)


class View(grok.View):
    grok.context(IMainSection)
    grok.require('zope2.View')
    grok.name('view')

    def constructImageTag(self):
        obj = aq_inner(self.context)
        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('image', width=870, height=421)
        data = {}
        if scale is not None:
            data['url'] = scale.url
            data['width'] = scale.width
            data['height'] = scale.height
        return data
