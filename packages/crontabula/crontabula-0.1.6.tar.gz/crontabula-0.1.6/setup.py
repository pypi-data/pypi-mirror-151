# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crontabula']

package_data = \
{'': ['*']}

extras_require = \
{'cli': ['click']}

entry_points = \
{'console_scripts': ['crontabula = crontabula.cli:cli']}

setup_kwargs = {
    'name': 'crontabula',
    'version': '0.1.6',
    'description': 'Parse crontab expressions with Python',
    'long_description': '# Crontabula 🧛\n\n[![PyPI version](https://badge.fury.io/py/crontabula.svg)](https://badge.fury.io/py/crontabula)\n\nCrontabula is a small library for parsing Crontab expressions into Python objects. The usage is simple:\n\n```python\nimport crontabula\n\ncrontab = crontabula.parse("*/10 3,6 * * 1-4")\nprint(crontab.next)\n# datetime.datetime(...)\n```\n\n## Installation\n\nInstall with:\n\n```\npip install crontabula\n```\n\n## CLI\n\nCrontabula comes with a small utility to print debug information about a crontab expression. Make sure you install the\nlibrary with the `cli` extra (`pip install "crontabula[cli]"`).\n\n```\n$ crontabula "*/15 * 1,15 * 1-5,6"\nminute         0 15 30 45\nhour           0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23\nday of month   1 15\nmonth          1 2 3 4 5 6 7 8 9 10 11 12\nday of week    1 2 3 4 5 6\nnext time      2022-04-19 17:30:00 (in 0:03:59.987874)\n```\n\n## Contributing\n\nConfigure the environment and run the tests using [Poetry](https://python-poetry.org/):\n\n```\n$ poetry install\n$ poetry run pre-commit install  # Optional, for linting with black\n$ poetry run pytest\n```\n',
    'author': 'Tom Forbes',
    'author_email': 'tom@tomforb.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/orf/crontabula',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
