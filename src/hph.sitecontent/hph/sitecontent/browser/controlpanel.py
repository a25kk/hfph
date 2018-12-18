# -*- coding: utf-8 -*-
"""Module providing control panel views"""
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from hph.sitecontent import MessageFactory as _


class HphBaseSettings(BrowserView):
    """ Ade25 settings overview """

    def update(self):
        if super(HphBaseSettings, self).update():
            if 'form.button.setup' in self.request.form:
                self.process_setup()

    def process_setup(self):
        IStatusMessage(self.request).addStatusMessage(
            _(u'Setup initialized.'), 'info')
