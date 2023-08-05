# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_tabbed_admin2',
 'django_tabbed_admin2.templatetags',
 'django_tabbed_admin2.tests']

package_data = \
{'': ['*'],
 'django_tabbed_admin2': ['static/tabbed_admin/css/*',
                          'static/tabbed_admin/css/images/*',
                          'static/tabbed_admin/js/*',
                          'templates/tabbed_admin/*']}

setup_kwargs = {
    'name': 'django-tabbed-admin2',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Attilio Greco',
    'author_email': 'attilio.greco.gapmilano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
