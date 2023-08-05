# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_filter',
 'fastapi_filter.base',
 'fastapi_filter.contrib',
 'fastapi_filter.contrib.mongoengine',
 'fastapi_filter.contrib.sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.78.0,<0.79.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'fastapi-filter',
    'version': '0.0.0',
    'description': 'FastAPI filter',
    'long_description': '[![Netlify Status](https://api.netlify.com/api/v1/badges/83451c4f-76dd-4154-9b2d-61f654eb0704/deploy-status)](https://app.netlify.com/sites/soft-sherbet-1c5dfd/deploys)\n',
    'author': 'Arthur Rio',
    'author_email': 'arthur.rio44@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arthurio/fastapi-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
