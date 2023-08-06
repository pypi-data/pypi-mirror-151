# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xmodmap_toggle']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['xmodmap_toggle = xmodmap_toggle.main:main']}

setup_kwargs = {
    'name': 'xmodmap-toggle',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Christoffer Aakre',
    'author_email': 'christoffer.corfield@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
