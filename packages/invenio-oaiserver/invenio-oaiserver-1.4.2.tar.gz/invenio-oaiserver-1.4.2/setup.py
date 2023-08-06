# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
# Copyright (C)      2021 Graz University of Technology.
# Copyright (C)      2021 TU Wien.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that implements OAI-PMH server."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'invenio-indexer>=1.2.2',
    'invenio-jsonschemas>=1.1.3',
    'invenio-marc21>=1.0.0a9',
    'mock>=1.3.0',
    'pytest-invenio>=1.4.1',
]

# Should follow inveniosoftware/invenio versions
invenio_db_version = '>=1.0.14,<2.0.0'
invenio_search_version = '>=1.4.2,<2.0.0'

extras_require = {
    'admin': [
        'invenio-admin>=1.3.0',
    ],
    'celery': [
        'invenio-celery>=1.2.3',
    ],
    'docs': [
        'Sphinx==4.5.0',
    ],
    # Elasticsearch version
    'elasticsearch6': [
        'invenio-search[elasticsearch6]{}'.format(invenio_search_version),
    ],
    'elasticsearch7': [
        'invenio-search[elasticsearch7]{}'.format(invenio_search_version),
    ],
    # Databases
    'mysql': [
        'invenio-db[mysql]{}'.format(invenio_db_version),
    ],
    'postgresql': [
        'invenio-db[postgresql]{}'.format(invenio_db_version),
    ],
    'sqlite': [
        'invenio-db{}'.format(invenio_db_version),
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name[0] == ':' or name in (
            'mysql', 'postgresql', 'sqlite',
            'elasticsearch6', 'elasticsearch7'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.8',
]

install_requires = [
    'arrow>=0.17.0',
    'dojson>=1.3.0',
    'invenio-base>=1.2.11',
    'invenio-i18n>=1.3.2',
    'invenio-pidstore>=1.2.2',
    'invenio-records>=1.6.0',
    'invenio-rest>=1.2.4',
    'lxml>=4.3.0',
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_oaiserver', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-oaiserver',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio OAI-PMH',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-oaiserver',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_oaiserver = invenio_oaiserver:InvenioOAIServer',
        ],
        'invenio_base.blueprints': [
            'invenio_oaiserver = invenio_oaiserver.views.server:blueprint',
        ],
        'invenio_base.api_apps': [
            'invenio_oaiserver = invenio_oaiserver:InvenioOAIServer',
        ],
        'invenio_db.alembic': [
            'invenio_oaiserver = invenio_oaiserver:alembic',
        ],
        'invenio_db.models': [
            'invenio_oaiserver = invenio_oaiserver.models',
        ],
        'invenio_admin.views': [
            'invenio_oaiserver = invenio_oaiserver.admin:set_adminview',
        ],
        'invenio_jsonschemas.schemas': [
            'oaiserver = invenio_oaiserver.schemas',
        ],
        'invenio_pidstore.minters': [
            'oaiid = invenio_oaiserver.minters:oaiid_minter',
        ],
        'invenio_pidstore.fetchers': [
            'oaiid = invenio_oaiserver.fetchers:oaiid_fetcher',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 5 - Production/Stable',
    ],
)
