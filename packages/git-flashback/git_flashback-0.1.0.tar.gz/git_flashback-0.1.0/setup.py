# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_flashback']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'git-flashback',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'yohan-pg',
    'author_email': 'pg.yohan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
