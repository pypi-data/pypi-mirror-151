# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zd',
 'zd.boop',
 'zd.boop.aws',
 'zd.test',
 'zd.test.aws',
 'zd.test.metrics',
 'zd.test.mock',
 'zd.test.timehelp',
 'zd.test.tools']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.23.4,<2.0.0',
 'datadog>=0.44.0,<0.45.0',
 'mock>=4.0.3,<5.0.0',
 'python-dateutil>=2.4.2',
 'pytz==2013.7']

setup_kwargs = {
    'name': 'zd.testt',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'michael-drozdov-zocdoc',
    'author_email': '86305671+michael-drozdov-zocdoc@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
