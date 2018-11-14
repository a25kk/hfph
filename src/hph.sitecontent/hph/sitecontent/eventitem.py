import datetime
from five import grok
from plone.directives import dexterity, form

from zope import schema

from plone.app.textfield import RichText

from hph.sitecontent import MessageFactory as _


class IEventItem(form.Schema):
    """
    An event with a start and end date
    """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    location = schema.TextLine(
        title=_(u"Event Location"),
        required=True,
    )
    start = schema.Datetime(
        title=_(u"Start date"),
        required=True,
    )
    end = schema.Datetime(
        title=_(u"End date"),
        required=True,
    )
    text = RichText(
        title=_(u"Event Description"),
        required=False,
    )


@form.default_value(field=IEventItem['start'])
def startDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(7)


@form.default_value(field=IEventItem['end'])
def endDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(10)


class EventItem(dexterity.Item):
    grok.implements(IEventItem)


class View(grok.View):
    grok.context(IEventItem)
    grok.require('zope2.View')
    grok.name('view')
