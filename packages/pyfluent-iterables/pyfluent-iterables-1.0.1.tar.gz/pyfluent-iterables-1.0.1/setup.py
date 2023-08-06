# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfluent_iterables']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfluent-iterables',
    'version': '1.0.1',
    'description': 'Fluent API wrapper for Python collections',
    'long_description': '# pyfluent-iterables\nFluent API wrapper for Python collections.\n',
    'author': 'Jan Michelfeit',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mifeet/pyfluent-iterables',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
