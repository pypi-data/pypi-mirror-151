# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tieto']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0', 'psycopg[binary,pool]>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'tieto',
    'version': '0.2.0',
    'description': 'A pretty face on Psycopg3.',
    'long_description': None,
    'author': 'Abram Isola',
    'author_email': 'abram@isola.mn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
