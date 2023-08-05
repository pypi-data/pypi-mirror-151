# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamunolib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'streamunolib',
    'version': '0.3.0',
    'description': 'Library of generic transform components.',
    'long_description': None,
    'author': 'Pierre Chanial',
    'author_email': 'pierre.chanial@apc.in2p3.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
