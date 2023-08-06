# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['summon']

package_data = \
{'': ['*']}

install_requires = \
['pluggy>=1.0.0,<2.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['summon = summon.__main__:main']}

setup_kwargs = {
    'name': 'summon-tasks',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tarcísio Eduardo Moreira Crocomo',
    'author_email': 'tarcisioe@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
