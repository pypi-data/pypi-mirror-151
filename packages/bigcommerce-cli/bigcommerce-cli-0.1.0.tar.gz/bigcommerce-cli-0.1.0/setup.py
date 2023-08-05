# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigcommerce_cli',
 'bigcommerce_cli.delete',
 'bigcommerce_cli.get',
 'bigcommerce_cli.post',
 'bigcommerce_cli.put',
 'bigcommerce_cli.settings',
 'bigcommerce_cli.utils',
 'bigcommerce_cli.utils.bigcommerce',
 'bigcommerce_cli.utils.bigcommerce.resources']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'prettytable>=3.3.0,<4.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['bcli = bigcommerce_cli.commands:bcli']}

setup_kwargs = {
    'name': 'bigcommerce-cli',
    'version': '0.1.0',
    'description': 'BigCommerce Management CLI',
    'long_description': None,
    'author': 'dhartle4',
    'author_email': 'dhartle4@uncc.edu',
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
