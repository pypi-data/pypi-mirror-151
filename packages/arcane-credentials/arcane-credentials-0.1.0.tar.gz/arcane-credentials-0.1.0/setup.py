# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane', 'arcane.credentials']

package_data = \
{'': ['*']}

install_requires = \
['arcane-core>=1.7.0,<2.0.0',
 'arcane-datastore>=1.1.0,<2.0.0',
 'arcane-secret>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'arcane-credentials',
    'version': '0.1.0',
    'description': 'Package description',
    'long_description': '# Arcane credentials README\n\n\n## Release history\nTo see changes, please see CHANGELOG.md\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
