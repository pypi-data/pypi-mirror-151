# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lamper_cli']

package_data = \
{'': ['*']}

install_requires = \
['boto3',
 'click',
 'colorama',
 'coloredlogs',
 'progressbar2',
 'requests',
 'terminaltables',
 'tqdm']

entry_points = \
{'console_scripts': ['lamper-cli = lamper_cli.cli:cli']}

setup_kwargs = {
    'name': 'lamper-cli',
    'version': '0.2.2',
    'description': 'An easy to use AWS Lambda Function enumeration tool with visual report',
    'long_description': '',
    'author': 'Sina Kheirkhah',
    'author_email': 'sina.for.sec@gmail.com',
    'maintainer': 'SinSinology',
    'maintainer_email': 'sina.for.sec@gmail.com',
    'url': 'https://github.com/mdsecresearch/lamper-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
