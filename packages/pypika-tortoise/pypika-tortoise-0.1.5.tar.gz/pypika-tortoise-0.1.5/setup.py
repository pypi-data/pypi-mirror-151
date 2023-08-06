# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypika', 'pypika.dialects']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypika-tortoise',
    'version': '0.1.5',
    'description': 'Forked from pypika and streamline just for tortoise-orm',
    'long_description': "# pypika-tortoise\n\n[![image](https://img.shields.io/pypi/v/pypika-tortoise.svg?style=flat)](https://pypi.python.org/pypi/pypika-tortoise)\n[![image](https://img.shields.io/github/license/tortoise/pypika-tortoise)](https://github.com/tortoise/pypika-tortoise)\n[![image](https://github.com/tortoise/pypika-tortoise/workflows/pypi/badge.svg)](https://github.com/tortoise/pypika-tortoise/actions?query=workflow:pypi)\n[![image](https://github.com/tortoise/pypika-tortoise/workflows/ci/badge.svg)](https://github.com/tortoise/pypika-tortoise/actions?query=workflow:ci)\n\nForked from [pypika](https://github.com/kayak/pypika) and streamline just for tortoise-orm.\n\n## Why forked?\n\nThe original repo include many databases that tortoise-orm don't need, and which aims to be a perfect sql builder and\nshould consider more compatibilities, but tortoise-orm is not, and we need add new features and update it ourselves.\n\n## What change?\n\nDelete many codes that tortoise-orm don't need, and add features just tortoise-orm considers to.\n\n## What affect tortoise-orm?\n\nNothing, because this repo keeps the original struct and code.\n\n## ThanksTo\n\n- [pypika](https://github.com/kayak/pypika), a python SQL query builder that exposes the full richness of the SQL\n  language using a syntax that reflects the resulting query.\n\n## License\n\nThis project is licensed under the [Apache-2.0](./LICENSE) License.\n",
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tortoise/pypika-tortoise',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
