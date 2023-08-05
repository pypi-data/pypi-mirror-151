# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nextx',
 'nextx.dependencies',
 'nextx.domain',
 'nextx.exceptions',
 'nextx.grpc',
 'nextx.grpc.protos',
 'nextx.interfaces',
 'nextx.pubsub',
 'nextx.repository']

package_data = \
{'': ['*']}

install_requires = \
['Inject>=4.3.1,<5.0.0',
 'aioredis>=2.0.1,<3.0.0',
 'beanie>=1.10.4,<2.0.0',
 'fastapi>=0.75.1,<0.76.0',
 'grpclib>=0.4.2,<0.5.0',
 'protobuf>=3.20.0,<4.0.0',
 'python-decouple>=3.6,<4.0',
 'python-jose>=3.3.0,<4.0.0',
 'uvicorn>=0.17.6,<0.18.0']

setup_kwargs = {
    'name': 'nextx',
    'version': '0.15.0',
    'description': 'Basic structure for fastapi microservices with specific support for blueprint project solution.',
    'long_description': None,
    'author': 'adriangs1996',
    'author_email': 'adriangonzalezsanchez1996@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
