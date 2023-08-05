# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cribbage']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'pytest>=6.1.2,<7.0.0', 'tqdm>=4.53.0,<5.0.0']

setup_kwargs = {
    'name': 'cribbage',
    'version': '1.3.2',
    'description': 'Cribbage for your command line',
    'long_description': None,
    'author': 'Alex Carlin',
    'author_email': 'alex@inkisbetter.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
