# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databutton_web']

package_data = \
{'': ['*'], 'databutton_web': ['local/*', 'local/assets/*']}

setup_kwargs = {
    'name': 'databutton-web',
    'version': '0.3.3',
    'description': '',
    'long_description': None,
    'author': 'Databutton',
    'author_email': 'hi@databutton.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
