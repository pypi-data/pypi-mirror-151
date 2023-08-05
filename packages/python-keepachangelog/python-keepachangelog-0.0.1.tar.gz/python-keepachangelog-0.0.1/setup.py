# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_keepachangelog']

package_data = \
{'': ['*']}

install_requires = \
['semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'python-keepachangelog',
    'version': '0.0.1',
    'description': 'Parser + generator for Changelogs of spec from https://keepachangelog.com/en/1.0.0/',
    'long_description': None,
    'author': 'Tom Whitwell',
    'author_email': 'tom@whi.tw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
