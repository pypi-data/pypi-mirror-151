# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlsx_evaluate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xlsx-evaluate',
    'version': '0.1.1',
    'description': 'Calculate XLSX formulas',
    'long_description': '# Calculate XLSX formulas\n\n[![CI](https://github.com/devind-team/xlsx_evaluate/workflows/Release/badge.svg)](https://github.com/devind-team/devind-django-dictionaries/actions)\n[![Coverage Status](https://coveralls.io/repos/github/devind-team/xlsx_evaluate/badge.svg?branch=main)](https://coveralls.io/github/devind-team/devind-django-dictionaries?branch=main)\n[![PyPI version](https://badge.fury.io/py/xlsx_evaluate.svg)](https://badge.fury.io/py/xlsx_evaluate)\n[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg)](https://opensource.org/licenses/MIT)\n\n\nThis library is fork [xlcalculator](https://github.com/bradbase/xlcalculator).\n\n',
    'author': 'Victor',
    'author_email': 'lyferov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devind-team/xlsx_evaluate',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
