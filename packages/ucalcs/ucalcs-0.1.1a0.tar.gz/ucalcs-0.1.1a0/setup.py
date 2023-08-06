# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ucalcs']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ucalcs = ucalcs.basics:main']}

setup_kwargs = {
    'name': 'ucalcs',
    'version': '0.1.1a0',
    'description': 'This is a library of simple math operations.',
    'long_description': '# uCALC FOR SIMPLE CALCULATIONS OF NUMBERS LIST\n---\n\n### This is a library of simple math operations.\n--- \n\n\n\n- You can pass a list of values \u200b\u200bso that it returns a result.\n\n- Use the methods (*some_all, subtract_all, multiply_all, divide_all*).\n\n- The calculation is done in the order sent.',
    'author': 'onezer00',
    'author_email': 'caimbe2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
