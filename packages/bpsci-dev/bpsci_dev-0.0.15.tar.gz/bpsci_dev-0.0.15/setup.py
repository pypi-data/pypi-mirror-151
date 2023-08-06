# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bpsci_dev']

package_data = \
{'': ['*'], 'bpsci_dev': ['assets/objects/*']}

install_requires = \
['numpy>=1.18.4,<2.0.0', 'pandas>=1.2.4,<2.0.0', 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'bpsci-dev',
    'version': '0.0.15',
    'description': '',
    'long_description': None,
    'author': 'Jerry Varghese',
    'author_email': 'varghese.jerryj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
