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
    'version': '0.1.1',
    'description': 'Async toolkit for advanced scheduling',
    'long_description': '# python-async-df\nTools for advanced asyncio scheduling and "depth-first" execution of async functions\n',
    'author': 'Kristján Valur Jónsson',
    'author_email': 'sweskman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kristjanvalur/py-asynkit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
