# -*- coding: utf-8 -*-
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

from hph.sitecontent import MessageFactory as _


class IExcludeFromFooterNavigationDefault(Interface):

    def __call__():
        """boolean if item is by default excluded from navigation or not.
        """


@implementer(IExcludeFromFooterNavigationDefault)
def default_exclude_false(context):
    """provide a default adapter with the standard uses
    """
    return False


@implementer(IExcludeFromFooterNavigationDefault)
def default_exclude_true(context):
    """provide a alternative adapter with opposite default as standard
    """
    return True


@provider(IContextAwareDefaultFactory)
def default_exclude(context):
    return IExcludeFromFooterNavigationDefault(context)


@provider(IFormFieldProvider)
class IExcludeFromFooterNavigation(model.Schema):
    """Behavior interface to exclude items from footer navigation.
    """

    model.fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['exclude_from_toc']
    )

    exclude_from_toc = schema.Bool(
        title=_(u'Exclude from footer navigation'
        ),
        description=_(u'If selected, this item will not appear in the '
                      u'table of contents listing in the site footer'
        ),
        defaultFactory=default_exclude,
        required=False,
    )

    directives.omitted('exclude_from_toc')
    directives.no_omit(IEditForm, 'exclude_from_toc')
    directives.no_omit(IAddForm, 'exclude_from_toc')
