# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastcrud']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[asyncio]>=1.4.36,<2.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'fastcrud',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ada0l',
    'author_email': 'andreika.varfolomeev@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
