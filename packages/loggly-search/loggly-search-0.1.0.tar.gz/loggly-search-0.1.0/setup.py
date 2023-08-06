# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loggly_search']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.5.3,<2.0.0', 'httpx>=0.22.0,<0.23.0', 'yarl>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['loggly-search = loggly_search.__main__:main']}

setup_kwargs = {
    'name': 'loggly-search',
    'version': '0.1.0',
    'description': 'A CLI for Loggly search',
    'long_description': "# loggly-search\nA CLI for Loggly search\n\n## Installation\n```\npip install loggly-search\n```\n\n## Configuration\nYou'll need both your account subdomain (ex. `myaccount` of `myaccount.loggly.com`) \nand an [API token](https://documentation.solarwinds.com/en/success_center/loggly/content/admin/token-based-api-authentication.htm) to use this tool.\nBoth of these can then be passed via the `--subdomain` and `--token` parameters or\nthrough the `LOGGLY_SUBDOMAIN` and `LOGGLY_TOKEN` environment variables.\n\n```\nloggly-search --subdomain myaccount --token abcxyz\n```\n\n## Usage Examples\n```\nloggly-search --from=-7d CRITERIA\n```\n\n```\nloggly-search --from '2022-05-17T08:00:00.000-04:00' --to '2022-05-17T10:00:00.000-04:00' CRITERIA\n```\n",
    'author': 'Andrew Rabert',
    'author_email': 'ar@nullsum.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
