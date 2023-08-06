# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['common', 'dbt', 'dbt.adapters.layer_bigquery', 'dbt.include.layer_bigquery']

package_data = \
{'': ['*'],
 'dbt.include.layer_bigquery': ['macros/original/*',
                                'macros/original/materializations/*']}

install_requires = \
['dbt-bigquery==1.0.0',
 'dbt-core==1.0.5',
 'layer-sdk>=0.9.355573',
 'sqlparse>=0.4.2,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['pandas==1.3.5'],
 ':python_version >= "3.8"': ['pandas>=1.4.2,<1.5.0']}

setup_kwargs = {
    'name': 'dbt-layer-bigquery',
    'version': '0.1.2352961172',
    'description': 'The Layer / BigQuery adapter plugin for dbt',
    'long_description': '# Layer dbt Adapter for BigQuery\n\nThis adapter runs dbt builds for ML pipelines with BigQuery as the backing data warehouse.\n',
    'author': 'Layer',
    'author_email': 'info@layer.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
