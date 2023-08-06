# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iuguclient']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'iuguclient',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Erick Duarte',
    'author_email': 'erickod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
