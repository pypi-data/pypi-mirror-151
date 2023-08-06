# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtxlog']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'redis>=4.3.1,<5.0.0']

setup_kwargs = {
    'name': 'dtxlog',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Youngbok Yoon',
    'author_email': 'bok@weltcorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
