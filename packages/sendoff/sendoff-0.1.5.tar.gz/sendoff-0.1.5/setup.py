# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sendoff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sendoff',
    'version': '0.1.5',
    'description': 'The minimal SDF metadata parser',
    'long_description': 'sendoff\n=======\n\n.. image:: https://results.pre-commit.ci/badge/github/pechersky/sendoff/main.svg\n   :target: https://results.pre-commit.ci/latest/github/pechersky/sendoff/main\n   :alt: pre-commit.ci status\n\n.. image:: https://github.com/pechersky/sendoff/actions/workflows/tox.yml/badge.svg\n   :target: https://github.com/pechersky/sendoff/actions/workflows/tox.yml\n   :alt: Tox status\n\nThe minimal SDF metadata parser.\n\nOften, SDFs have lots of useful metadata on them in the title and record fields/values.\nHowever, reading a molecule (via rdkit, OpenEye toolkits, etc) can be slow because those\nlibraries also construct the molecules. Modifying the metadata, or filtering/sorting based\non the metadata also can induce non-idempotent differences in the file based on\nopinionated approaches in chemical libraries.\n\nThis library strives to be able to handle SDF files even with malformed chemistry or\nmetadata. Since much debugging of our files and data deals with such files, having access\nto simple tools to interrogate the files while not modifying the file is crucial.\n\nThis package also tried to document the "canonical" ways metadata is handled by the larger\npackages. To wit, there are tests to monitor how, for example, rdkit deals with molecules\nthat have multiline record values, or a "$$$$" molecule title.\n',
    'author': 'Yakov Pechersky',
    'author_email': 'ypechersky@treeline.bio',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pechersky/sendoff',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
