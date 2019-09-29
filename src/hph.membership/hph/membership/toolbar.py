from five import grok
from plone import api
from urllib import unquote
from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import Interface
from zope.browsermenu.interfaces import IBrowserMenu
from zope.traversing.interfaces import ITraversable
from plone.app.layout.viewlets.interfaces import IPortalHeader
from plone.memoize.instance import memoize

from hph.membership.interfaces import IHPHMembershipTool


class ToolbarViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(IHPHMembershipTool)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalHeader)
    grok.name('hph.membership.ToolbarViewlet')

    def update(self):
        self.context = aq_inner(self.context)
        self.tools = self.get_multi_adapter(u'plone_tools')
        self.context_state = self.get_multi_adapter(u'plone_context_state')
        self.portal_state = self.get_multi_adapter(u'plone_portal_state')
        self.anonymous = self.portal_state.anonymous()

        self.context_url = self.context.absolute_url()
        self.context_fti = self.context.getTypeInfo()
        self.request_url = self.request.get('ACTUAL_URL', '')

        request_url_path = self.request_url[len(self.context_url):]
        if request_url_path.startswith('/'):
            request_url_path = request_url_path[1:]
        self.request_url_path = request_url_path

    def get_multi_adapter(self, name):
        return getMultiAdapter((self.context, self.request), name=name)

    def is_deco_enabled(self):
        try:
            from plone.app.blocks.layoutbehavior import ILayoutAware
            if ILayoutAware.providedBy(self.context):
                return True
        except:
            pass
        return False

    @memoize
    def actions(self):
        if 'disable_border' in self.request:
            return []
        actions = []

        # 'folder' actions
        if self.context_state.is_structural_folder():
            actions.extend(self.context_state.actions('folder'))

        # 'object' actions
        actions.extend(self.context_state.actions('object'))

        # sort actions
        sort_order = ['folderContents']

        def sort_actions(action):
            try:
                return sort_order.index(action['id'])
            except ValueError:
                return 255
        actions.sort(key=sort_actions)

        # content actions (eg. Contents, Edit, View, Sharing...)
        result = []
        active_action_found = False
        for action in actions:
            item = action

            # deco edit button should have a bit different id
            if item['id'] == 'edit' and self.is_deco_enabled():
                item['id'] = 'deco'

            # make sure id is unique
            item['id'] = 'plone-action-' + item['id']

            # we force that view is open in parent
            if item['id'] == 'view':
                item['link_target'] = '_parent'

            # button url
            button_url = action['url'].strip()
            if (button_url.startswith('http') or
                    button_url.startswith('javascript')):
                item['url'] = button_url
            else:
                item['url'] = '%s/%s' % (self.context_url, button_url)

            # Action method may be a method alias:
            # Attempt to resolve to a template.
            action_method = item['url'].split('/')[-1]
            action_method = self.context_fti.queryMethodID(
                action_method, default=action_method)

            # Determine if action is activated
            if action_method:
                request_action = unquote(self.request_url_path)
                request_action = self.context_fti.queryMethodID(
                    request_action, default=request_action)
                if action_method == request_action:
                    item['klass'] = 'active'
                    active_action_found = True

            result.append(item)

        if not active_action_found:
            for action in result:
                if action['id'] == 'plone-toolbar-action-view':
                    action['klass'] = 'active'

        return result

    @memoize
    def contentmenu(self):
        if 'disable_border' in self.request:
            return []

        def contentmenu(items):
            buttons = []
            for item in items:
                item['id'] = ''
                item['klass'] = ''
                if 'extra' in item:
                    if 'id' in item['extra'] and item['extra']['id']:
                        item['id'] = item['extra']['id']
                    if 'class' in item['extra'] and item['extra']['class']:
                        if item['extra']['class'] == 'actionMenuSelected':
                            item['klass'] = 'active'
                        else:
                            if 'stateTitle' not in item['extra']:
                                item['klass'] = item['extra']['class']
                    if 'submenu' in item and item['submenu']:
                        item['submenu'] = contentmenu(item['submenu'])
                buttons.append(item)
            return buttons

        plone_contentmenu = getUtility(IBrowserMenu,
                                       name='plone_contentmenu').getMenuItems
        return contentmenu(plone_contentmenu(self.context, self.request))

    @memoize
    def user_displayname(self):
        """Get the username of the currently logged in user
        """

        if self.anonymous:
            return None

        member = self.portal_state.member()
        userid = member.getId()

        membership = self.tools.membership()
        memberInfo = membership.getMemberInfo(userid)

        fullname = userid

        # Member info is None if there's no Plone user object, as when using
        # OpenID.
        if memberInfo is not None:
            fullname = memberInfo.get('fullname', '') or fullname

        return fullname

    @memoize
    def user_portrait(self):
        member = self.portal_state.member()
        membership = self.tools.membership()
        portrait = membership.getPersonalPortrait(member.getId())
        if portrait is not None:
            return portrait.absolute_url()

    @memoize
    def user_homeurl(self):
        member = api.user.get_current()
        userid = member.getId()
        return "%s/ws/%s" % (self.portal_state.navigation_root_url(),
                             userid)

    @memoize
    def user_actions(self):
        actions = self.context_state.actions('user')
        return [item for item in actions if item['available']]

    def show_cms_tools(self):
        context = aq_inner(self.context)
        admin_roles = ('Manager', 'Site Administrator', 'StaffMember',
                       'Contributor', 'Editor')
        admin_groups = ('Administrators', 'Site Administrators',
                        'staff', 'Staff')
        is_adm = False
        user = api.user.get_current()
        userid = user.getId()
        if userid is 'zope-admin':
            is_adm = True
        roles = api.user.get_roles(username=userid, obj=context)
        for role in roles:
            if role in admin_roles:
                is_adm = True
        groups = api.group.get_groups(username=userid)
        for group in groups:
            if group in admin_groups:
                is_adm = True
        return is_adm


class UnthemedRequest(object):
    implements(ITraversable)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        if self.request is not None:
            self.request.response.setHeader('X-Theme-Disabled', 'True')
            self.request['HTTP_X_THEME_ENABLED'] = False
        return self.context
