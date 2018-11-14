import logging
from five import grok
from plone import api

from ZODB.POSException import ConflictError
from plone.uuid.interfaces import IUUID
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent

logger = logging.getLogger(__name__)


@grok.subscribe(IUserLoggedInEvent)
def logged_in_handler(event):
    """
    Listen to the login event and perform a redirect to the users
    workspace
    """
    user = event.object
    portal = api.portal.get()
    memberfolder = portal['ws']
    mf_url = memberfolder.absolute_url()
    request = getattr(portal, "REQUEST", None)
    if not request:
        return False
    try:
        request.response.redirect(mf_url)
    except ConflictError:
        # Transaction retries must be
        # always handled specially in exception handlers
        raise
    except Exception, e:
        # Let the login proceed even if the folder has been deleted
        # don't make it impossible to login to the site
        logger.exception(e)
        return False
    return request.response.redirect(mf_url)
