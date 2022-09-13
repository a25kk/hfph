# -*- coding: utf-8 -*-
"""Module providing workspace browser views"""
from Acquisition import aq_inner
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.keyring import django_random
from plone.memoize.view import memoize
from zope.component import getMultiAdapter

from hph.lectures.lecture import ILecture

from hph.membership import MessageFactory as _



class WorkSpaceView(BrowserView):
    """ Workspace view """

    def __call__(self, **kw):
        self.flash_msg = self.display_welcome_msg()
        self.has_personel_contents = len(self.personal_contents()) > 0
        self.has_contributing_content = len(self.contributing()) > 0
        self.has_worklist = len(self.worklist()) > 0
        return self.render()

    def render(self):
        return self.index()

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
        info['worklist'] = user.getProperty('worklist', list())
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
        return IContentListing(brains[:10])

    @staticmethod
    def course_folders():
        context = api.content.get(UID='66f5d7ff29ae45779726e640d5a57e55')
        folders = context.restrictedTraverse('@@folderListing')(
            portal_type='hph.lectures.coursefolder',
            review_state='published')
        return folders

    def get_current_semester_lectures_container(self):
        sub_folders = self.course_folders()
        for folder in sub_folders:
            container = folder.getObject()
            current_marker = getattr(container, 'is_current_semester', None)
            if current_marker:
                return folder
        return sub_folders[0]

    @memoize
    def _lectures(self):
        container = self.get_current_semester_lectures_container()
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
        if len(self.worklist()):
            results = self.worklist()
        else:
            for item in self._lectures():
                if context.getId() in item.getObject().listContributors():
                    info = {}
                    info['uid'] = api.content.get_uuid(obj=item.getObject())
                    info['title'] = item.Title
                    info['url'] = '{0}/@@lecture-factory/{1}'.format(
                        context.absolute_url(),
                        api.content.get_uuid(obj=item.getObject()))
                    info['path'] = self.breadcrumbs(item)
                    results.append(info)
        return results

    def worklist(self):
        context = aq_inner(self.context)
        userinfo = self.user_info()
        user_worklist = userinfo['worklist']
        removable = []
        worklist = []
        for item_uid in user_worklist:
            try:
                item = api.content.get(UID=item_uid)
                info = {}
                info['uid'] = item_uid
                info['title'] = item.Title()
                if ILecture.providedBy(item):
                    next_url = '{0}/@@lecture-factory/{1}'.format(
                        context.absolute_url(), item_uid)
                    info['url'] = next_url
                else:
                    info['url'] = item.absolute_url()
                info['path'] = self.breadcrumbs(item)
                worklist.append(info)
            except:
                removable.append(item_uid)
        if len(removable):
            removed = self._autoclean_worklist(removable)
            msg = _(u"Removed {0} broken assignments from worklist".format(
                removed))
            api.portal.show_message(message=msg, request=self.request)
        return worklist

    def _autoclean_worklist(self, items):
        context = aq_inner(self.context)
        idx = 0
        user_worklist = self.user_info()['worklist']
        # Make sure the user work list is an actual list
        updated = list(user_worklist)
        for item in items:
            idx += 1
            updated.remove(item)
        user_id = context.getId()
        user = api.user.get(username=user_id)
        user.setMemberProperties(mapping={'worklist': updated})
        return idx

    def breadcrumbs(self, item):
        """ Compute nice breadcrumb for object location in site """
        try:
            obj = item.getObject()
        except AttributeError:
            obj = item
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

