# hph.widgets

## HPH Content Widgets

* `Source code @ GitHub <https://github.com/kreativkombinat/hph.widgets>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/hph.widgets>`_
* `Documentation @ ReadTheDocs <http://hphwidgets.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/kreativkombinat/hph.widgets>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

The generated Python package holds an example content type `ContentPage` which
provides a folderish version of the default **Page** document type.

The implementation is kept simple on purpose and asumes that the developer will
add further content manually.


## Installation

To install `hph.widgets` you simply add ``hph.widgets``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `hph.widgets` using the Add-ons control panel.
