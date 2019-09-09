# -*- coding: utf-8 -*-
"""Module providing embeddable social sharing bar"""
from requests import utils
from Acquisition import aq_inner
from Products.Five import BrowserView
from ade25.base.interfaces import IContentInfoProvider
from requests.utils import requote_uri


class SocialSharing(BrowserView):
    """ Embeddable card view for news entries"""

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def content_snippet(item, text_field):
        content_info_provider = IContentInfoProvider(item)
        text_snippet = content_info_provider.teaser_text(
            text_field, characters=120)
        return text_snippet

    @property
    def settings(self):
        context = aq_inner(self.context)
        data = {
            "facebook": {
                "url": "https://www.facebook.com/sharer/sharer.php?u=",
                "text": ""
            },
            "twitter": {
                "url": "https://twitter.com/intent/tweet?url=",
                "text": "&text={0}".format(
                    self.content_snippet(context, context.Title()),
                )
            },
            "xing": {
                "url": "https://www.xing.com/spi/shares/new?url=",
                "text": ""
            },
            "linkedin": {
                "url": "https://www.linkedin.com/shareArticle?mini=true&url=",
                "text": "&title={0}&summary={1}".format(
                    self.content_snippet(context, context.Title()),
                    self.content_snippet(context, context.Description())
                )
            }
        }
        return data

    def share_link(self, service=None):
        context = aq_inner(self.context)
        settings = self.settings
        share_link = context.absolute_url()
        if service:
            service_details = settings[service]
            share_link = "{share_link}{url}{text}".format(
                share_link=service_details['url'],
                url=context.absolute_url(),
                text=service_details['text']
            )
        return requote_uri(share_link)
