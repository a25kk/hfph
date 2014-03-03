from five import grok
from plone import api

from plone.uuid.interfaces import IUUID
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent


@grok.subscribe(IUserLoggedInEvent)
def logged_in_handler(event):
    """
    Listen to the login event and perform a redirect to the users
    workspace
    """
    user = event.object
    portal = api.portal.get()
    memberfolder = api.content.get(path='/user')
    mfuid = api.content.get_uuid(obj=memberfolder)
    uuid = user.getProperty('workspace', memberfolder_uid)
    workspace = api.content.get(UID=uuid)
    ws_url = workspace.absolute_url()
    request = getattr(portal, "REQUEST", None)
    if not request:
        return False
    try:
        target = portal.unrestrictedTraverse(CUSTOM_USER_FOLDERS)
    except ConflictError:
        # Transaction retries must be
        # always handled specially in exception handlers
        raise
    except Exception, e:
        # Let the login proceed even if the folder has been deleted
        # don't make it impossible to login to the site
        logger.exception(e)
        return False
    return request.response.redirect(ws_url)
