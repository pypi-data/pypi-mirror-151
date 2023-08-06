# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['art_dl', 'art_dl.sites', 'art_dl.sites.deviantart', 'art_dl.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiohttp-socks[asyncio]>=0.7.1,<0.8.0',
 'aiohttp>=3.8.1,<4.0.0',
 'lxml>=4.8.0,<5.0.0']

setup_kwargs = {
    'name': 'art-dl',
    'version': '0.1.0',
    'description': 'Artworks downloader',
    'long_description': None,
    'author': 'Ilia',
    'author_email': 'istudyatuni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
