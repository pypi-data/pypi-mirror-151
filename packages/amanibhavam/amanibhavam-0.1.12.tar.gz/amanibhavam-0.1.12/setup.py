# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amanibhavam']

package_data = \
{'': ['*']}

install_requires = \
['cdktf-cdktf-provider-aws>=7.0.55,<8.0.0',
 'cdktf-cdktf-provider-digitalocean>=0.0.40,<0.0.41',
 'cdktf-cdktf-provider-null>=0.6.55,<0.7.0',
 'cdktf>=0.10.4,<0.11.0',
 'defn-cdktf-provider-buildkite>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['amanibhavam = config:main']}

setup_kwargs = {
    'name': 'amanibhavam',
    'version': '0.1.12',
    'description': '',
    'long_description': None,
    'author': 'Amanibhavam',
    'author_email': 'iam@defn.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
