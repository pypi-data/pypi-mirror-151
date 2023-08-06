# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tapipy_tapisservice',
 'tapipy_tapisservice.tapisdjango',
 'tapipy_tapisservice.tapisfastapi',
 'tapipy_tapisservice.tapisflask']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tapipy-tapisservice',
    'version': '1.1.0',
    'description': "Python lib for interacting with an instance of the Tapis API Framework's tapisservice plugin.",
    'long_description': 'Tapipy plugin granting Tapis service functionality using `import tapisservice`.',
    'author': 'Joe Stubbs',
    'author_email': 'jstubbs@tacc.utexas.edu',
    'maintainer': 'Joe Stubbs',
    'maintainer_email': 'jstubbs@tacc.utexas.edu',
    'url': 'https://github.com/tapis-project/tapipy-tapisservice',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
