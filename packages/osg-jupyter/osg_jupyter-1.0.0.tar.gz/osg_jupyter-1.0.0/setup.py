# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osg', 'osg.jupyter']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.7,<1.8',
 'PyYAML>=5.4,<5.5',
 'cryptography>=3.3.2,<3.4',
 'kubernetes>=12.0,<12.1',
 'ldap3>=2.8,<2.9']

setup_kwargs = {
    'name': 'osg-jupyter',
    'version': '1.0.0',
    'description': 'Support for OSG for Project Jupyter',
    'long_description': None,
    'author': 'Brian Aydemir',
    'author_email': 'baydemir@morgridge.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brianaydemir/osg-jupyter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
