# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ndix', 'ndix.src']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ndix',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'michael',
    'author_email': 'michael.d.moor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
