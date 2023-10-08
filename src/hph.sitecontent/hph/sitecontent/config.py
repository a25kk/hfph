# -*- coding: utf-8 -*-
"""Module providing package configuration"""

NAVIGATION_CLOSE_ELEMENT = u'<svg class="app-nav__toggle-icon" id="nav-toggle-close" xmlns="http://www.w3.org/2000/svg" version="1.1" width="100%" height="100%" viewBox="0 0 36 36"><polygon fill-rule="evenodd" points="27.8999.515 26.485 8.101 18 16.586 9.514 8.101 8.1 9.515 16.586 18 8.1 26.486 9.514 27.9 18 19.414 26.485 27.9 27.899 26.486 19.414 18"></polygon></svg>'  # noqa


NAVIGATION_OPEN_ELEMENT = u'<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 36 36"><polygon fill-rule="evenodd" points="14.707 26.707 13.293 25.293 20.586 18 13.293 10.707 14.707 9.293 23.414 18"/></svg>'  #noqa


def navigation_elements(action=None):
    if action == 'open':
        return NAVIGATION_OPEN_ELEMENT
    else:
        return NAVIGATION_CLOSE_ELEMENT
