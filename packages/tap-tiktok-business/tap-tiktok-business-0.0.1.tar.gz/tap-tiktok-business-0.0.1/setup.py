# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_tiktok_business', 'tap_tiktok_business.tests']

package_data = \
{'': ['*'], 'tap_tiktok_business': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.4.9,<0.5.0']

entry_points = \
{'console_scripts': ['tap-tiktok-business = '
                     'tap_tiktok_business.tap:TapTiktokBusiness.cli']}

setup_kwargs = {
    'name': 'tap-tiktok-business',
    'version': '0.0.1',
    'description': '`tap-tiktok-business` is a Singer tap for the Tiktok Business API, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Hunter Kuffel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
