# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fava_envelope', 'fava_envelope.modules', 'fava_envelope.templates']

package_data = \
{'': ['*']}

install_requires = \
['fava>=1.14,<2.0', 'pandas>=1.2.1,<2.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'fava-envelope',
    'version': '0.5.3',
    'description': 'Fava Envelope budgeting for beancount',
    'long_description': None,
    'author': 'Brian Ryall',
    'author_email': 'bryall@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bryall/fava-envelope',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
