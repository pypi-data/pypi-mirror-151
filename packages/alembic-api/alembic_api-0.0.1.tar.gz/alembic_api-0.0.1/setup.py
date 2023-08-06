# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alembic_api']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.36,<2.0.0', 'alembic>=1.7.7,<2.0.0']

setup_kwargs = {
    'name': 'alembic-api',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'dotX12',
    'author_email': 'hash@shitposting.team',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
