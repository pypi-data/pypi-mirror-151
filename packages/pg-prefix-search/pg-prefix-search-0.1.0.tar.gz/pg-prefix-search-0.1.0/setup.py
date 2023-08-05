# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pg_prefix_search', 'pg_prefix_search.migrations', 'pg_prefix_search.scripts']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0', 'Unidecode>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'pg-prefix-search',
    'version': '0.1.0',
    'description': 'Text search by word fragments using Postgres-specific indices.',
    'long_description': None,
    'author': 'Szymon Sobczak',
    'author_email': 'szymon@solvbot.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
