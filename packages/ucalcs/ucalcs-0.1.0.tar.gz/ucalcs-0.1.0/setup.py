# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ucalcs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ucalcs',
    'version': '0.1.0',
    'description': 'This is a library of simple math operations.',
    'long_description': None,
    'author': 'onezer00',
    'author_email': 'caimbe2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
