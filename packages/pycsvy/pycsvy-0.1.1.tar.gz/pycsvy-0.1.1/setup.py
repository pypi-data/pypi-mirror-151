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
    'version': '0.1.1',
    'description': 'Python reader/writer for CSV files with YAML header information.',
    'long_description': '# CSVY for Python\n\n[![Test and build](https://github.com/ImperialCollegeLondon/csvy/actions/workflows/ci.yml/badge.svg)](https://github.com/ImperialCollegeLondon/csvy/actions/workflows/ci.yml)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/pycsvy.svg)](https://pypi.python.org/pypi/pycsvy/)\n[![PyPI status](https://img.shields.io/pypi/status/pycsvy.svg)](https://pypi.python.org/pypi/pycsvy/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pycsvy.svg)](https://pypi.python.org/pypi/pycsvy/)\n[![PyPI license](https://img.shields.io/pypi/l/pycsvy.svg)](https://pypi.python.org/pypi/pycsvy/)\n\nCSV is a popular format for storing tabular data used in many disciplines. Metadata concerning the contents of the file is often included in the header, but it rarely follows a format that is machine readable - sometimes is not even human readable! In some cases, such information is provided in a separate file, which is not ideal as it is easy for data and metadata to get separated.\n\nCSVY is a small Python package to handle CSV files in which the metadata in the header is formatted in YAML. It supports reading/writing tabular data contained in numpy arrays, pandas DataFrames and nested lists, as well as metadata using a standard python dictionary. Ultimately, it aims to incorporate information about the CSV dialect used and a Table Schema specifying the contents of each column to aid the reading and interpretation of the data.\n',
    'author': 'Diego',
    'author_email': 'd.alonso-alvarez@imperial.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ImperialCollegeLondon/pycsvy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
