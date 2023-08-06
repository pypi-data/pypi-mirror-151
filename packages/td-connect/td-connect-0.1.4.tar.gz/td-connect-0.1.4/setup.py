# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['td_connect']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.36,<2.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'psycopg2>=2.9.3,<3.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'ready-logger>=0.1.0,<0.2.0',
 'requests>=2.26.0,<3.0.0',
 'websockets>=10.1,<11.0']

entry_points = \
{'console_scripts': ['create_td_app_table = '
                     'td_connect.td_connect:create_app_table',
                     'print_td_app_config = '
                     'td_connect.td_connect:print_app_config']}

setup_kwargs = {
    'name': 'td-connect',
    'version': '0.1.4',
    'description': 'Authentication manager for TD Ameritrade REST APIs.',
    'long_description': None,
    'author': 'Dan Kelleher',
    'author_email': 'dan@danklabs.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
