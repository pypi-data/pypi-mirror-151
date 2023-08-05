# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mccabe_cli']

package_data = \
{'': ['*']}

install_requires = \
['mccabe>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['mccabe = mccabe_cli:main']}

setup_kwargs = {
    'name': 'mccabe-cli',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/mccabe-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
