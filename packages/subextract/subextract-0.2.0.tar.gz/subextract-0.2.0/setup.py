# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subextract']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'langcodes>=3.3.0,<4.0.0']

entry_points = \
{'console_scripts': ['subextract = subextract.cli:main']}

setup_kwargs = {
    'name': 'subextract',
    'version': '0.2.0',
    'description': 'CLI for easy extraction of subtitles from mkv files',
    'long_description': None,
    'author': 'disrupted',
    'author_email': 'hi@salomonpopp.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
