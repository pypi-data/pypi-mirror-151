# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vfx_fs_util', 'vfx_fs_util.compressed_filepath']

package_data = \
{'': ['*']}

install_requires = \
['Lucidity>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'vfx-fs-util',
    'version': '0.1.1',
    'description': 'A library to help with filesystem management in the VFX industry.',
    'long_description': None,
    'author': 'John Andrews',
    'author_email': 'johnandrews@macvanderlay.lan',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
