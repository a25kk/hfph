# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form, directives
from plone.app.z3cform.widget import LinkFieldWidget
from zope import schema
from zope.interface import Interface, provider
from plone.namedfile import field as named_file

from ade25.panelpage import MessageFactory as _


@provider(IFormFieldProvider)
class IHPHWidgetTeaserEvents(Interface):
    """ Content Widget Teaser Events """

    title = schema.TextLine(
        title=_("Event Teaser Headline"),
        required=False
    )
    directives.widget(link=LinkFieldWidget)
    link = schema.TextLine(
        title=_(u"Event Teaser Link"),
        description=_(u"Please select link target for global read more action. "
                      u"Leave empty to fall back to the global event calendar"
                      u" link."),
        required=False,
    )


@provider(IFormFieldProvider)
class IHPHWidgetTeaserLinksInternal(Interface):
    """ Content Widget Teaser Links internal """

    title = schema.TextLine(
        title=_("Teaser Links Internal Headline"),
        required=False
    )


@provider(IFormFieldProvider)
class IHPHWidgetLinkInternal(Interface):
    """ Content Panel Storage Slots """

    title = schema.TextLine(
        title=_("Internal Link Title"),
        required=False
    )
    form.widget('icon', klass='js-choices-selector')
    icon = schema.Choice(
        title=_(u"Link Icon"),
        description=_(u"Select adequate icon for the linked section"),
        required=False,
        default='widget--tile',
        vocabulary='hph.widgets.vocabularies.TeaserLinkIconOptions'
    )
    directives.widget(link=LinkFieldWidget)
    link = schema.TextLine(
        title=_(u"Link"),
        description=_(u"Please select link target"),
        required=False,
    )


@provider(IFormFieldProvider)
class IHPHWidgetTeaserLinksExternal(Interface):
    """ Content Widget Teaser Links internal """

    title = schema.TextLine(
        title=_("Teaser Links External Headline"),
        required=False
    )


@provider(IFormFieldProvider)
class IHPHWidgetLinkExternal(Interface):
    """ Content Panel Storage Slots """

    title = schema.TextLine(
        title=_("External Link Title"),
        required=False
    )
    image = named_file.NamedBlobImage(
        title=_(u"Image"),
        required=True
    )
    image_caption = schema.TextLine(
        title=_(u"Image Copyright Information"),
        required=False
    )
    directives.widget(link=LinkFieldWidget)
    link = schema.TextLine(
        title=_(u"Link"),
        description=_(u"Please select link target"),
        required=False,
    )

