# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nops_kafka']

package_data = \
{'': ['*']}

install_requires = \
['kafka_python>2.0.0', 'msgpack>1.0.0']

setup_kwargs = {
    'name': 'nops-kafka',
    'version': '0.2.0',
    'description': 'Kafka tooling used in nOps.io',
    'long_description': None,
    'author': 'nOps Engineers',
    'author_email': 'eng@nops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
