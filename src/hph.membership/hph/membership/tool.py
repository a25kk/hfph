import socket
import requests
import contextlib
import smtplib
from five import grok
from plone import api
from zope.interface import Interface


DEFAULT_SERVICE = 'http'
DEFAULT_SERVICE_URI = 'serverdetails.json'
DEFAULT_SERVICE_TIMEOUT = socket.getdefaulttimeout()


class IMemberTool(Interface):
    """ Call processing and optional session data storage entrypoint """

    def status(context):
        """ Check availability of external service

        @param timeout: Set status request timeout
        @param service: Service type e.g. tcp
        @param host:    Hostname of the component node
        @param payload: Pass additional parameters e.g. auth tokens
        """


class MemberTool(grok.GlobalUtility):
    grok.provides(IMemberTool)

    def status(self,
               hostname=None,
               service=DEFAULT_SERVICE,
               timeout=DEFAULT_SERVICE_TIMEOUT,
               **kwargs):
        info = {}
        info['name'] = service
        if service == 'smtp':
            smtp = smtplib.SMTP()
            response = smtp.connect(hostname)
            info['code'] = response[0]
            info['status'] = 'active'
        else:
            url = 'http://{0}'.format(hostname)
            with contextlib.closing(requests.get(url)) as response:
                r = response
                sc = r.status_code
                info['code'] = sc
                if sc == requests.codes.ok:
                    info['status'] = 'active'
                else:
                    info['code'] = 'unreachable endpoint'
        return info

    def get(self,
            hostname=None,
            path_info=DEFAULT_SERVICE_URI,
            timeout=DEFAULT_SERVICE_TIMEOUT, **kwargs):
        service_url = 'http://{0}'.format(hostname)
        url = service_url + '/{0}'.format(path_info)
        with contextlib.closing(requests.get(url)) as response:
            r = response
            if r.status_code == requests.codes.ok:
                return r.json()
