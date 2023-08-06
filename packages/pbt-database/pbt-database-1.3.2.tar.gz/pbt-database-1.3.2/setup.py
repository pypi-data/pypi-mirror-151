# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['database', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.36,<2.0.0', 'asyncpg==0.25.0', 'psycopg2-binary==2.9.3']

setup_kwargs = {
    'name': 'pbt-database',
    'version': '1.3.2',
    'description': 'Database driver',
    'long_description': '[![N|Solid](https://294904.selcdn.ru/git/logo.png)](https://portalbilet.ru/)\n## Database driver\n\nProvide PostgresSQL Model built-ins with i18n support.\n\nUse as package with service core and setup with env variables.\n\n## Maintain\nUse poetry for all:\n```sh\npoetry install\npoetry build\npoetry publish\n```\n\n## CI/CD Options\n\n| option          | type  | info     |\n| -----           | ----- | -----    |\n| **DB_HOST**       | str   |  Host    |\n| **DB_PORT**       | int   |  Port    |\n| **DB_NAME**       | str   | Database |\n| **DB_USER**       | str   | Username |\n| **DB_PASSWORD**   | str   | Password |\n\n\n## Testing\n```.sh\npytest tests\n```\n| :warning: Check database connection before launch - all data will be erased!|\n|-----------------------------------------------------------------------------|\n\n## License\n```\nMIT © PortalBilet Team, 2022\n```\n',
    'author': 'everhide',
    'author_email': 'i.tolkachnikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
