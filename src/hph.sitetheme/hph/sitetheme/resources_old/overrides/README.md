Overrides directory for plone.app.themingplugins
================================================

You should preferable use this directory to override Plone and Plone Addon
templates, by copying the original template and renaming it to the full
dotted name.

Usage example:
--------------

For example, to override logo.pt in plone.app.layout.viewlets, which is found
in plone/app/layout/viewlets/logo.pt inside the plone.app.layout distribution,
you would copy logo.pt into the overrides directory as

`plone.app.layout.viewlets.logo.pt.

You can then modify this as required.

Note: Templates are loaded at Zope startup.
In debug mode, template changes are reflected on the fly, but you will need to
restart Zope to pick up new templates.
