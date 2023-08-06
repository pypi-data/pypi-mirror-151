# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ichika_utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0',
 'numba>=0.55.1,<0.56.0',
 'pandas>=1.4.2,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'uvloop>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'ichika-utils',
    'version': '0.1.4.dev0',
    'description': 'Asynchronous Statistics Utils for Ichika',
    'long_description': '# Ichika Utils\n\nA set of utils used by Ichika. This is not production ready, and not even ready for anything. this is highly experimental.',
    'author': 'No767',
    'author_email': '73260931+No767@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/No767/Ichika-Utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
