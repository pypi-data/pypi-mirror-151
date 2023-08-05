# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_intro',
 'fastapi_intro.authentication',
 'fastapi_intro.database',
 'fastapi_intro.tests']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.36,<2.0.0',
 'fastapi>=0.76.0,<0.77.0',
 'passlib[bcrypt]>=1.7.4,<2.0.0',
 'pydantic[email]>=1.9.0,<2.0.0',
 'pytest==7.1.2',
 'python-jose[cryptography]>=3.3.0,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn[standard]>=0.17.6,<0.18.0']

setup_kwargs = {
    'name': 'fastapi-intro',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'prabal',
    'author_email': 'prabal01pathak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
