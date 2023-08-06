# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['defn_cdktf_provider_buildkite',
 'defn_cdktf_provider_buildkite.buildkite',
 'defn_cdktf_provider_buildkite.buildkite._jsii']

package_data = \
{'': ['*']}

install_requires = \
['cdktf>=0.10.4,<0.11.0']

setup_kwargs = {
    'name': 'defn-cdktf-provider-buildkite',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Amanibhavam',
    'author_email': 'iam@defn.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
