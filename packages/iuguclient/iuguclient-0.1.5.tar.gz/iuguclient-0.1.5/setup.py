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
    'version': '0.1.5',
    'description': '',
    'long_description': '# Iugu\n\nThe Iugu provides a Python REST APIs to create, process and manage payments.\n\n## Installation\n\nUsing pip:\n\n    $ pip install iuguclient\n\n## Usage\n\nYou should import and create an iugu instance using your [api token](https://dev.iugu.com/reference#section-criando-suas-chaves-de-api-api-tokens):\n\n```py\nimport iugu\napi = iugu.config(token=IUGU_API_TOKEN)\n```\n\nAfter that you can use the instance to iniciate the module you need, example:\n\n```py\n# token api\niugu_token_api = iugu.Token()\n# customer api\niugu_customer_api = iugu.Customer()\n```\n\nTo see all available modules, check the [iugu folder](https://github.com/iugu/iugu-python/tree/master/iugu) of this project.\n\n## Documentation\n\nVisit [iugu.com/referencias/api](http://iugu.com/referencias/api) for api reference or [iugu.com/documentacao](http://iugu.com/documentacao) for full documentation\n\n\n## Original project\nhttps://github.com/iugu/iugu-python',
    'author': 'Erick Duarte',
    'author_email': 'erickod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/erickod/iugu-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
