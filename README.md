# hfph

This repository holds the configuration and site packages for the hfph application.


## Upgrade Guide (4->5)

Packages to uninstall:

- plone.app.drafts
- plone.app.widgets

Rename portal title: the unicode conversion for the control panel breaks due
the non convertable umlaut characters
