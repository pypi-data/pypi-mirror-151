# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_icomoon']

package_data = \
{'': ['*'], 'wagtail_icomoon': ['templates/icons/*']}

install_requires = \
['wagtail>=2.16']

setup_kwargs = {
    'name': 'wagtail-icomoon',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Seb',
    'author_email': 'seb@neonjungle.studio',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
