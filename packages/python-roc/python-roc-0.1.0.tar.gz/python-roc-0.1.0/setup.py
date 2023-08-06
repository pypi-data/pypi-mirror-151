# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_roc']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib==3.3.4', 'numpy==1.19.5', 'scipy==1.1.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'python-roc',
    'version': '0.1.0',
    'description': 'ROC curve visualization tool',
    'long_description': None,
    'author': 'Petro Liashchynskyi',
    'author_email': 'p.liashchynskyi@apiko.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
