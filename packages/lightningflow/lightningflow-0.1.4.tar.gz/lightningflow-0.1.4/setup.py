# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lightningflow']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.8,<3.0']

setup_kwargs = {
    'name': 'lightningflow',
    'version': '0.1.4',
    'description': 'A workflow template designed for optical transceiver test.',
    'long_description': None,
    'author': 'Chongjun Lei',
    'author_email': 'chongjun.lei@neophotonics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/asakiasako/LIGHTNINGFLOW',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
