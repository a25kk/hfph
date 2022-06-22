import datetime
# from five import grok
from z3c.form import form
from plone.namedfile.field import NamedBlobImage
from plone.supermodel.directives import fieldset

from zope import schema

from plone.app.textfield import RichText

from hph.sitecontent import MessageFactory as _


class IEventItem(form.Schema):
    """
    An event with a start and end date
    """
    location = schema.TextLine(
        title=_(u"Event Location"),
        required=True,
    )
    event_type = schema.Choice(
        title=_(u"Event Type"),
        vocabulary="hph.sitecontent.EventTypes",
        required=False,
    )
    start = schema.Datetime(
        title=_(u"Start date"),
        required=True,
    )
    end = schema.Datetime(
        title=_(u"End date"),
        required=True,
    )
    full_day = schema.Bool(
        title=_(u"Full Day"),
        required=False,
        default=False
    )
    open_end = schema.Bool(
        title=_(u"Open End"),
        required=False,
        default=False
    )
    fieldset(
        'details',
        label=_(u"Details"),
        fields=['text', ]
    )
    text = RichText(
        title=_(u"Event Description"),
        required=False,
    )

    fieldset(
        'media',
        label=_(u"Media"),
        fields=['image', 'image_caption']
    )

    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload preview image that can be used in search "
                      u"results and listings."),
        required=False
    )

    image_caption = schema.TextLine(
        title=_(u"Cover Image Caption"),
        required=False
    )
    fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['featured', 'promoted']
    )
    featured = schema.Bool(
        title=_(u"Featured item"),
        description=_(u"Select to mark this item for featured display on "
                      u"overview pages like for example the parent container."),
        default=False,
        required=False
    )

    promoted = schema.Bool(
        title=_(u"Promote to front page"),
        description=_(u"Select to mark this item for display on the sites "
                      u"front page. Note: the number of displayed items on the "
                      u"front page might be limited or ordered by publication "
                      u"date and the selection does not force the item to be "
                      u"promoted in any case."),
        default=False,
        required=False
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
