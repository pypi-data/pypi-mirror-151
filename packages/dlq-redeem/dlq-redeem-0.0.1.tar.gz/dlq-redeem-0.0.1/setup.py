# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlq_redeem']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.23,<2.0', 'click-log>=0.4.0,<0.5.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['redeem = dlq_redeem.cli:cli']}

setup_kwargs = {
    'name': 'dlq-redeem',
    'version': '0.0.1',
    'description': 'AWS SQS dead letter queue (DLQ) message inspection and cleanup automation tool',
    'long_description': '<h2 align="center">dlq-redeem</h2>\n<p align="center">\n<a href="https://pypi.org/project/dlq-redeem/"><img alt="PyPI" src="https://img.shields.io/pypi/v/dlq-redeem"></a>\n<a href="https://pypi.org/project/dlq-redeem/"><img alt="Python" src="https://img.shields.io/pypi/pyversions/dlq-redeem.svg"></a>\n<a href="https://github.com/epsylabs/dlq-redeem/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/dlq-redeem.svg"></a>\n</p>\nAWS SQS dead letter queue (DLQ) message inspection and cleanup automation tool\n\n## Installation\n```shell\npip install dlq-redeem\n```\n\n## What is it about?\n`dlq-redeem` allows you to go through, interactively, DLQ messages and decide if you want te reprocess them.\n\nBased on type of message it will either move it back to its source SQS or invoke lambda function in case message was an EventBridge event.\n',
    'author': 'Epsy',
    'author_email': 'engineering@epsyhealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/epsylabs/dlq-redeem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
