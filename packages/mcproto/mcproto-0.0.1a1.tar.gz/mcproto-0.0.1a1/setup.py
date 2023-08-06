# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcproto', 'mcproto.protocol', 'mcproto.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcproto',
    'version': '0.0.1a1',
    'description': 'Library providing easy interactions with minecraft sevrers',
    'long_description': None,
    'author': 'ItsDrike',
    'author_email': 'itsdrike@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
