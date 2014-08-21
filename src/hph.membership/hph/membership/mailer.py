# -*- coding: UTF-8 -*-
""" Module providing utility functions for composing and sending
    html and plaintext messages
"""
import cStringIO
import formatter
import logging
import lxml
import os
import socket

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.utils import formataddr
from email.utils import parseaddr
from htmllib import HTMLParser
from lxml.html.clean import Cleaner
from smtplib import SMTPException
from string import Template

from plone import api
from zope.component import getMultiAdapter
from Products.MailHost.MailHost import MailHostError

from Products.CMFPlone.utils import getSiteEncoding
from Products.CMFPlone.utils import safe_unicode

logger = logging.getLogger('hph.membership')

DEFAULT_CHARSET = 'utf-8'


def send_mail(message, addresses, subject, immediate=True):
    """Send a notification email to the list of addresses.

    Each message is passed without change to the mail host.  It should
    probably be a correctly encoded Message or MIMEText.
    """
    mail_host = get_mail_host()
    if mail_host is None:
        logger.warn("Cannot send notification email: please configure "
                    "MailHost correctly.")

    mfrom = get_mail_from_address()
    header_charset = get_charset()

    for address in addresses:
        if not address:
            continue
        try:
            mail_host.send(message,
                           mto=address,
                           mfrom=mfrom,
                           subject=subject,
                           immediate=immediate,
                           charset=header_charset)
        except (socket.error, SMTPException, MailHostError):
            logger.warn('Could not send email to %s with subject %s',
                        address, subject)
        except:
            raise


def get_charset():
    """Character set to use for encoding the email.
    """
    charset = None
    portal = api.portal.get()
    if portal is None:
        return DEFAULT_CHARSET
    charset = portal.getProperty('email_charset', '')
    if not charset:
        charset = getSiteEncoding(portal)
    return charset


def su(value):
    """Return safe unicode version of value.
    """
    return safe_unicode(value, encoding=get_charset())


def get_mail_host():
    """Get the MailHost object.

    Return None in case of problems.
    """
    portal = api.portal.get()
    if portal is None:
        return None
    request = portal.REQUEST
    ctrlOverview = getMultiAdapter((portal, request),
                                   name='overview-controlpanel')
    mail_settings_correct = not ctrlOverview.mailhost_warning()
    if mail_settings_correct:
        mail_host = api.portal.get_tool(name='MailHost')
        return mail_host


def get_mail_from_address():
    portal = api.portal.get()
    if portal is None:
        return ''
    from_address = portal.getProperty('email_from_address', '')
    from_name = portal.getProperty('email_from_name', '')
    mfrom = formataddr((from_name, from_address))
    if parseaddr(mfrom)[1] != from_address:
        # formataddr probably got confused by special characters.
        mfrom = from_address
    return mfrom


def get_mail_template(name, data=dict()):
    template_file = os.path.join(os.path.dirname(__file__), name)
    template = Template(open(template_file).read())
    composed = template.substitute(data)
    return composed


def prepare_email_message(message, plaintext):
    plain = plaintext
    html = message
    if not html:
        return None

    plain = su(plain)
    html = su(html)

    # We must choose the body charset manually.  Note that the
    # goal and effect of this loop is to determine the
    # body_charset.
    for body_charset in 'US-ASCII', get_charset(), 'UTF-8':
        try:
            plain.encode(body_charset)
            html.encode(body_charset)
        except UnicodeEncodeError:
            pass
        else:
            break
    # Encoding should work now; let's replace errors just in case.
    plain = plain.encode(body_charset, 'replace')
    html = html.encode(body_charset, 'xmlcharrefreplace')

    text_part = MIMEText(plain, 'plain', body_charset)
    html_part = MIMEText(html, 'html', body_charset)

    # No sense in sending plain text and html when we only have
    # one of those:
    if not plain:
        return html_part
    if not html:
        return text_part

    # Okay, we send both plain text and html
    email_msg = MIMEMultipart('alternative')
    email_msg.epilogue = ''
    email_msg.attach(text_part)
    email_msg.attach(html_part)
    return email_msg


def create_plaintext_message(message):
        """ Create clean plain text version of email message

            Parse the html and remove style and javacript tags and then
            create a plain-text-message by parsing the html
            and attaching links as endnotes
        """
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        cleaner.kill_tags = ['style']
        doc = message.decode('utf-8', 'ignore')
        to_clean = lxml.html.fromstring(doc)
        cleaned_msg = lxml.html.tostring(cleaner.clean_html(to_clean))
        plain_text_maxcols = 72
        textout = cStringIO.StringIO()
        formtext = formatter.AbstractFormatter(formatter.DumbWriter(
                                               textout, plain_text_maxcols))
        parser = HTMLParser(formtext)
        parser.feed(cleaned_msg)
        parser.close()
        # append the anchorlist at the bottom of a message
        # to keep the message readable.
        counter = 0
        anchorlist = "\n\n" + ("-" * plain_text_maxcols) + "\n\n"
        for item in parser.anchorlist:
            counter += 1
            if item.startswith('https://'):
                new_item = item.replace('https://', 'http://')
            else:
                new_item = item
            anchorlist += "[%d] %s\n" % (counter, new_item)
        text = textout.getvalue() + anchorlist
        del textout, formtext, parser, anchorlist
        return text
