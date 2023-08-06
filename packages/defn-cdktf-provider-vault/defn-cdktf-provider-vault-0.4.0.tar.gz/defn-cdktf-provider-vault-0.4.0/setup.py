# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['defn_cdktf_provider_vault',
 'defn_cdktf_provider_vault.vault',
 'defn_cdktf_provider_vault.vault._jsii']

package_data = \
{'': ['*']}

install_requires = \
['cdktf>=0.10.4,<0.11.0']

setup_kwargs = {
    'name': 'defn-cdktf-provider-vault',
    'version': '0.4.0',
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
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
