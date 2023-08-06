# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quest',
 'quest.contrib',
 'quest.examples',
 'quest.examples.contrib',
 'quest.examples.images',
 'quest.examples.images.island',
 'quest.examples.images.items',
 'quest.examples.images.people']

package_data = \
{'': ['*'], 'quest.examples.images': ['racing/*']}

install_requires = \
['Shapely>=1.8.2,<2.0.0',
 'arcade==2.6.9',
 'easing-functions>=1.0.4,<2.0.0',
 'numpy>=1.22.3,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'xvfbwrapper>=0.2.9,<0.3.0']

setup_kwargs = {
    'name': 'questgame',
    'version': '0.2.2',
    'description': "Quest provides a simpler interface to python's Arcade library.",
    'long_description': None,
    'author': 'Chris Proctor',
    'author_email': 'github.com@accounts.chrisproctor.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cproctor/quest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
