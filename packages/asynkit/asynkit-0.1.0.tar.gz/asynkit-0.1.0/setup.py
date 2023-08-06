# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asynkit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asynkit',
    'version': '0.1.0',
    'description': 'Async toolkit for advanced scheduling',
    'long_description': None,
    'author': 'Kristján Valur Jónsson',
    'author_email': 'sweskman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
