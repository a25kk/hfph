# -*- coding: UTF-8 -*-
from Acquisition import aq_inner
from five import grok
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.dexterity.content import Container
from plone.directives import form
from plone.keyring import django_random
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.memoize.view import memoize
from zope.component import getMultiAdapter

from hph.lectures.lecture import ILecture

from hph.membership import MessageFactory as _


class IWorkspace(form.Schema, IImageScaleTraversable):
    """
    Personal workspace container for members
    """


class Workspace(Container):
    grok.implements(IWorkspace)
    pass


class View(grok.View):
    grok.context(IWorkspace)
    grok.require('cmf.ModifyPortalContent')
    grok.name('view')

    def update(self):
        self.flash_msg = self.display_welcome_msg()
        self.has_personel_contents = len(self.personal_contents()) > 0
        self.has_contributing_content = len(self.contributing()) > 0

    def display_welcome_msg(self):
        return self.request.get('welcome_msg', False)

    def user_info(self):
        context = aq_inner(self.context)
        info = {}
        userid = context.getId()
        user = api.user.get(username=userid)
        info['fullname'] = user.getProperty('fullname', '') or userid
        info['email'] = user.getProperty('email', _(u"No email provided"))
        info['login_time'] = user.getProperty('last_login_time', '')
        info['enabled'] = user.getProperty('enabled', '')
        info['confirmed'] = user.getProperty('confirmed', '')
        return info

    def is_staff(self):
        context = aq_inner(self.context)
        admin_roles = ('Manager', 'Site Administrator', 'StaffMember')
        is_adm = False
        user = api.user.get_current()
        userid = user.getId()
        if userid is 'zope-admin':
            is_adm = True
        roles = api.user.get_roles(username=userid, obj=context)
        for role in roles:
            if role in admin_roles:
                is_adm = True
        return is_adm

    def group_actions(self):
        context = aq_inner(self.context)
        userid = context.getId()
        groups = api.group.get_groups(username=userid)
        has_actions = ['Gasthoerer', 'Studierende', 'Alumni', 'prophil',
                       'Lehrende']
        actions = []
        for group in groups:
            if group.getName() in has_actions:
                gid = group.getId()
                info = {}
                info['group'] = group
                info['title'] = gid
                info['description'] = self._get_description(gid)
                info['action'] = self._get_action(gid)
                actions.append(info)
        return actions

    def _get_action(self, group):
        portal_url = api.portal.get().absolute_url()
        url = '{0}/ws'.format(portal_url)
        if group in ('Gasthoerer', 'Studierende'):
            url = '{0}/studium/lehrveranstaltungen'.format(portal_url)
        if group == 'Alumni':
            url = '{0}/studium/studentisches-leben/alumni'.format(portal_url)
        if group == 'prophil':
            url = '{0}/pro-philosophia'.format(portal_url)
        if group == 'Lehrende':
            url = '{0}/hochschule/lehrende/'.format(portal_url)
        return url

    def _get_description(self, group):
        desc = _(u'Standard description for workspace links')
        if group in ('Gasthoerer', 'Studierende'):
            desc = _(u'Students and guests description')
        if group == 'Alumni':
            desc = _(u'Alumni description')
        if group == 'prophil':
            desc = _(u'Prophil description')
        if group == 'Lehrende':
            desc = _(u'Lectures description')
        return desc

    def personal_contents(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        userid = context.getId()
        brains = catalog(Creator=userid)
        return IContentListing(brains)

    @memoize
    def _lectures(self):
        container = api.content.get(UID='66f5d7ff29ae45779726e640d5a57e55')
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(object_provides=ILecture.__identifier__,
                        path=dict(query='/'.join(container.getPhysicalPath()),
                                  depth=1),
                        review_state='published',
                        sort_on='courseNumber')
        return items

    def contributing(self):
        context = aq_inner(self.context)
        results = []
        for item in self._lectures():
            if context.getId() in item.getObject().listContributors():
                results.append(item)
        return results

    def breadcrumbs(self, item):
        obj = item.getObject()
        view = getMultiAdapter((obj, self.request), name='breadcrumbs_view')
        # cut off the item itself
        breadcrumbs = list(view.breadcrumbs())[:-1]
        if len(breadcrumbs) == 0:
            # don't show breadcrumbs if we only have a single element
            return None
        if len(breadcrumbs) > 3:
            # if we have too long breadcrumbs, emit the middle elements
            empty = {'absolute_url': '', 'Title': unicode('…', 'utf-8')}
            breadcrumbs = [breadcrumbs[0], empty] + breadcrumbs[-2:]
        return breadcrumbs

    def compose_pwreset_link(self):
        context = aq_inner(self.context)
        user_id = context.getId()
        user = api.user.get(username=user_id)
        token = self._access_token(user)
        portal_url = api.portal.get().absolute_url()
        url = '{0}/useraccount/{1}/{2}'.format(
            portal_url, user_id, token)
        return url

    def _access_token(self, user):
        stored_token = user.getProperty('token', '')
        if len(stored_token):
            token = stored_token
        else:
            token = django_random.get_random_string(length=12)
            user.setMemberProperties(mapping={'token': token})
        return token
