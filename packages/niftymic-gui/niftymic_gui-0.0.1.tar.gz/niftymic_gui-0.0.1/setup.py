# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niftymic_gui']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'rich>=12.4.1,<13.0.0']

entry_points = \
{'console_scripts': ['niftymic-gui = niftymic_gui.main:main']}

setup_kwargs = {
    'name': 'niftymic-gui',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'TonyChG',
    'author_email': 'tonychg7@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
