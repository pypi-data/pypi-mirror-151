# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csotools_serverquery',
 'csotools_serverquery.common',
 'csotools_serverquery.connection']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'csotools-serverquery',
    'version': '0.4.0',
    'description': 'Query GoldSource and CSO servers for server info, players and more',
    'long_description': None,
    'author': 'AnggaraNothing',
    'author_email': 'anggarayamap@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
