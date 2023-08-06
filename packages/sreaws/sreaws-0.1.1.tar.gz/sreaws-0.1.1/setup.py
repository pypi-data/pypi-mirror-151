# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sreaws']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sreaws',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'ccdale',
    'author_email': 'chris.allison@hivehome.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
