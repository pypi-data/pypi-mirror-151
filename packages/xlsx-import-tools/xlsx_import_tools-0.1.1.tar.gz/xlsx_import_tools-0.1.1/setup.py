# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlsx_import_tools', 'xlsx_import_tools.migrations']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.9,<4.0.0']

setup_kwargs = {
    'name': 'xlsx-import-tools',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Josh Brooks',
    'author_email': 'josh@catalpa.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
