# -*- coding: utf-8 -*-
"""Installer for the hph.widgets package."""

import os

from setuptools import find_packages, setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = read('README.rst')

setup(
    name='hph.widgets',
    version='1.0.0',
    description="HPH Content Widgets",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Plone, Python',
    author='Kreativkombinat GbR',
    author_email='info@kreativkombinat.de',
    url='http://pypi.python.org/pypi/hph.widgets',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['hph'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
