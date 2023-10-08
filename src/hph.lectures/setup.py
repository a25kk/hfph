import os

from setuptools import find_packages, setup


version = '1.0.0'

setup(name='hph.lectures',
      version=version,
      description="HPH listing of lectures",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Vorwaerts Werbung GbR',
      author_email='cb@vorwaerts-werbung.de',
      url='http://dist.vorwaerts-werbung.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['hph'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity [relations]',
          'plone.app.relationfield',
          'plone.namedfile [blobs]',
          'collective.z3cform.datagridfield',
          'plone.formwidget.contenttree',
          'plone.formwidget.autocomplete',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
