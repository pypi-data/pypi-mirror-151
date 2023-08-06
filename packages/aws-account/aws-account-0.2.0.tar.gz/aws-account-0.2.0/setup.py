# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_account', 'aws_account.test']

package_data = \
{'': ['*']}

install_requires = \
['boto3<1.23.3',
 'click>=8.0.3',
 'colorama>=0.4',
 'mypy-boto3-iam<=1.22.10',
 'mypy-boto3-sso<=1.22.10',
 'mypy-boto3-sts<=1.22.10']

entry_points = \
{'console_scripts': ['aws-account = aws_account.cli:main']}

setup_kwargs = {
    'name': 'aws-account',
    'version': '0.2.0',
    'description': 'Print out AWS account and identity information to verify which account/organization is currently in use.',
    'long_description': None,
    'author': 'M. Rollwagen',
    'author_email': 'rollwagen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rollwagen/aws-account',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
