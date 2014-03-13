from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone import api

from zope import schema

from zope.schema.vocabulary import getVocabularyRegistry

from plone.indexer import indexer
from plone.directives import form
from plone.dexterity.content import Container

from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.contentlisting.interfaces import IContentListing
from hph.publications.publication import IPublication

from hph.faculty import MessageFactory as _


class IFacultyMember(form.Schema, IImageScaleTraversable):
    """
    A faculty staff member
    """
    last_name = schema.TextLine(
        title=_(u"Lastname"),
        description=_(u"Provide last name for better filtering and search"),
        required=True,
    )
    lastname = schema.TextLine(
        title=_(u"Lastname"),
        description=_(u"Provide last name for better filtering and search"),
        required=True,
    )
    academicRole = schema.Choice(
        title=_(u"Accademic Role or Position"),
        vocabulary=u'hph.faculty.academicRole',
        required=True,
    )
    sidenote = schema.TextLine(
        title=_(u"Sidenote"),
        description=_(u"Optional additional information/sidenote"),
        required=False,
    )
    department = schema.TextLine(
        title=_(u"Department"),
        required=True,
    )
    street = schema.TextLine(
        title=_(u"Street"),
        required=False,
    )
    city = schema.TextLine(
        title=_(u"City"),
        required=False,
    )
    phone = schema.TextLine(
        title=_(u"Phone"),
        required=False,
    )
    fax = schema.TextLine(
        title=_(u"Fax"),
        required=False,
    )
    email = schema.TextLine(
        title=_(u"E-Mail"),
        required=False,
    )
    image = NamedBlobImage(
        title=_(u"Portrait Image"),
        required=False,
    )
    text = RichText(
        title=_(u"Body Text"),
        required=False,
    )
    publications = RelationList(
        title=u"Related Publication Items",
        default=[],
        value_type=RelationChoice(
            title=_(u"Publication"),
            source=ObjPathSourceBinder()),
        required=False,
    )


@indexer(IFacultyMember)
def lastNameIndexer(obj):
    return obj.lastname
grok.global_adapter(lastNameIndexer, name="lastname")


@indexer(IFacultyMember)
def academicRoleIndexer(obj):
    return obj.academicRole
grok.global_adapter(academicRoleIndexer, name="academicRole")


class FacultyMember(Container):
    grok.implements(IFacultyMember)


class View(grok.View):
    """ Faculty member view """
    grok.context(IFacultyMember)
    grok.require('zope2.View')
    grok.name('view')

    def parent_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def content_filter(self):
        context = aq_inner(self.context)
        container = aq_parent(context)
        tmpl = container.restrictedTraverse('@@content-filter-faculty')()
        return tmpl

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def computed_klass(self, value):
        context = aq_inner(self.context)
        active_filter = getattr(context, 'academicRole', None)
        klass = 'nav-item-plain'
        if active_filter == value:
            klass = 'active'
        return klass

    def show_address(self):
        context = aq_inner(self.context)
        display = False
        if context.street or context.email:
            display = True
        return display


class Publications(grok.View):
    grok.context(IFacultyMember)
    grok.require('zope2.View')
    grok.name('publications')

    def update(self):
        self.has_publications = len(self.publications()) > 0

    def parent_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def filter_options(self):
        context = aq_inner(self.context)
        vr = getVocabularyRegistry()
        vocab = vr.get(context, 'hph.faculty.academicRole')
        return vocab

    def computed_klass(self, value):
        context = aq_inner(self.context)
        active_filter = getattr(context, 'academicRole', None)
        klass = 'nav-item-plain'
        if active_filter == value:
            klass = 'active'
        return klass

    def publications(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        obj_provides = IPublication.__identifier__
        author_name = getattr(context, 'lastname')
        query = dict(object_provides=obj_provides,
                     lastname=author_name,
                     review_state='published')
        results = catalog.searchResults(query)
        return IContentListing(results)
