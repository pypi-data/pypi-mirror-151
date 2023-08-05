# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mamimo', 'mamimo.datasets']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'pandas>=1.4.2,<2.0.0', 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'mamimo',
    'version': '0.4.0',
    'description': 'A package to compute a marketing mix model.',
    'long_description': '# MaMiMo\nThis is a small library that helps you with your everyday **Ma**rketing **Mi**x **Mo**delling. It contains a few saturation functions, carryovers and some utilities for creating with time features.\n\nGive it a try via `pip install mamimo`!',
    'author': 'Garve',
    'author_email': 'xgarve@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Garve/mamimo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
