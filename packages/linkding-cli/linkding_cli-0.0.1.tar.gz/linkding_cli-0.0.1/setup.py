# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.commands', 'src.helpers']

package_data = \
{'': ['*']}

install_requires = \
['aiolinkding>=2022.5.0', 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['linkding = src.main:APP']}

setup_kwargs = {
    'name': 'linkding-cli',
    'version': '0.0.1',
    'description': 'A CLI to interact with a linkding instance',
    'long_description': '# 🔖 linkding-cli: A CLI to interact with a linkding instance\n\n[![CI](https://github.com/bachya/linkding-cli/workflows/CI/badge.svg)](https://github.com/bachya/linkding-cli/actions)\n[![PyPi](https://img.shields.io/pypi/v/linkding-cli.svg)](https://pypi.python.org/pypi/linkding-cli)\n[![Version](https://img.shields.io/pypi/pyversions/linkding-cli.svg)](https://pypi.python.org/pypi/linkding-cli)\n[![License](https://img.shields.io/pypi/l/linkding-cli.svg)](https://github.com/bachya/linkding-cli/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/linkding-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/linkding-cli)\n[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/linkding-cli/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n`linkding-cli` is a CLI to interact with a linkding instance.\n\n- [Installation](#installation)\n- [Python Versions](#python-versions)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n# Installation\n\n```python\npip install linkding-cli\n```\n\n# Python Versions\n\n`linkding-cli` is currently supported on:\n\n* Python 3.8\n* Python 3.9\n* Python 3.10\n\n# Usage\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/linkding-cli/issues)\n  or [initiate a discussion on one](https://github.com/bachya/linkding-cli/issues/new).\n2. [Fork the repository](https://github.com/bachya/linkding-cli/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `nox -rs coverage`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/linkding-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
