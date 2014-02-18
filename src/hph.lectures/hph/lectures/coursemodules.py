from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.directives import form
from zope import schema
from zope.interface import alsoProvides

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow

from hph.lectures import MessageFactory as _


class ICourseModules(model.Schema):
    """
        Schema for course modules
    """
    degree = schema.Choice(
        title=_(u"Degree"),
        description=_(u"Please select module degree"),
        vocabulary=u'hph.lectures.CourseDegree',
        required=True,
    )
    info = schema.TextLine(
        title=_(u"Module Information"),
        description=_(u"Enter corresponding product detail value"),
        required=True,
    )


class ICourseModuleInformation(model.Schema):
    """
       Marker/Form interface for Module Information
    """
    form.fieldset(
        'modules',
        label=u"Modules",
        fields=['moduledetails']
    )

    form.widget(moduledetails=DataGridFieldFactory)
    moduledetails = schema.List(
        title=u'Product Details',
        value_type=DictRow(
            title=u'Module Details',
            schema=ICourseModules),
        required=True
    )


alsoProvides(ICourseModuleInformation, IFormFieldProvider)
