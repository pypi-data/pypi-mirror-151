# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycsvy']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'pycsvy',
    'version': '0.1.0',
    'description': 'Library that implement saving/loading together tabular data and yaml-formatted metadata.',
    'long_description': None,
    'author': 'Diego',
    'author_email': 'd.alonso-alvarez@imperial.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
