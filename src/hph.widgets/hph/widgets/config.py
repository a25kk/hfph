# -*- coding: utf-8 -*-
"""Module providing widget setting constants"""

PKG_WIDGETS = {
    "hph-image-poster": {
        "pkg": "hph.widgets",
        "id": "hph-image-poster",
        "name": "HfPH Poster Image",
        "title": "Poster Image",
        "category": "more",
        "type": "content-item",
        "schema": "hph.widgets.widgets.image.interfaces.IHPHWidgetImagePoster",  # noqa
        "node": {}
    },
    "hph-teaser-events": {
        "pkg": "hph.widgets",
        "id": "hph-teaser-events",
        "name": "HfPH Teaser Events",
        "title": "Teaser Events",
        "category": "more",
        "type": "base",
        "schema": "",
        "node": {}
    },
    "hph-teaser-links": {
        "pkg": "hph.widgets",
        "id": "hph-teaser-links",
        "name": "HfPH Teaser Links",
        "title": "Teaser Links Internal",
        "category": "more",
        "type": "collection",
        "schema": "hph.widgets.widgets.teaser.interfaces.IHPHWidgetTeaserLinksInternal",  # noqa
        "node": {
            "title": "Teaser Internal Link",
            "schema": "hph.widgets.widgets.teaser.interfaces.IHPHWidgetLinkInternal"  # noqa
        }
    },
    "hph-slider": {
        "pkg": "hph.widgets",
        "id": "hph-slider",
        "name": "HfPH Slider",
        "title": "Slider",
        "category": "more",
        "type": "collection",
        "schema": "hph.widgets.widgets.slider.interfaces.IHPHWidgetSlider",  # noqa
        "node": {
            "title": "Teaser Internal Link",
            "schema": "hph.widgets.widgets.teaser.interfaces.IHPHWidgetLinkInternal"  # noqa
        }
    }
}
