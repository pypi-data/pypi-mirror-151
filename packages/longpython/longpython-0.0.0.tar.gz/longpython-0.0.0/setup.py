# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['longpython']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['longpython = longpython.main:main']}

setup_kwargs = {
    'name': 'longpython',
    'version': '0.0.0',
    'description': 'CLI tool to print long python',
    'long_description': None,
    'author': 'Hibiki(4513ECHO)',
    'author_email': '4513echo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4513ECHO/longpython',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
