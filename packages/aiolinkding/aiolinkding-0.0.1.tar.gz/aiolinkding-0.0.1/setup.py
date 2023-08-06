# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiolinkding']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0']

setup_kwargs = {
    'name': 'aiolinkding',
    'version': '0.0.1',
    'description': 'A Python3, async interface to the linkding REST API',
    'long_description': '# 🚰 aiolinkding: DESCRIPTION\n\n[![CI](https://github.com/bachya/aiolinkding/workflows/CI/badge.svg)](https://github.com/bachya/aiolinkding/actions)\n[![PyPi](https://img.shields.io/pypi/v/aiolinkding.svg)](https://pypi.python.org/pypi/aiolinkding)\n[![Version](https://img.shields.io/pypi/pyversions/aiolinkding.svg)](https://pypi.python.org/pypi/aiolinkding)\n[![License](https://img.shields.io/pypi/l/aiolinkding.svg)](https://github.com/bachya/aiolinkding/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/aiolinkding/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/aiolinkding)\n[![Maintainability](https://api.codeclimate.com/v1/badges/189379773edd4035a612/maintainability)](https://codeclimate.com/github/bachya/aiolinkding/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\nDESCRIPTION\n\n- [Installation](#installation)\n- [Python Versions](#python-versions)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n# Installation\n\n```python\npip install aiolinkding\n```\n\n# Python Versions\n\n`aiolinkding` is currently supported on:\n\n* Python 3.8\n* Python 3.9\n* Python 3.10\n\n# Usage\n\n## Creating a Client\n\nIt\'s easy to create an API client for a linkding instance. All you need are two\nparameters:\n\n1. A URL to a linkding instance\n2. A linkding API token\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom aiolinkding import Client\n\n\nasync def main() -> None:\n    """Create the aiohttp session and run the example."""\n    client = Client("http://127.0.0.1:8000", "token_abcde12345")\n\n\nasyncio.run(main())\n```\n\n## Working with Bookmarks\n\nThe `Client` object provides easy access to several bookmark-related API operations:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom aiolinkding import Client\n\n\nasync def main() -> None:\n    """Create the aiohttp session and run the example."""\n    client = Client("http://127.0.0.1:8000", "token_abcde12345")\n\n    # Get all bookmarks:\n    bookmarks = await client.bookmarks.async_all()\n    # >>> { "count": 5, "next": null, "previous": null, "results": [...] }\n\n\nasyncio.run(main())\n```\n\nBy default, the library creates a new connection to linkding with each coroutine. If you\nare calling a large number of coroutines (or merely want to squeeze out every second of\nruntime savings possible), an\n[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection\npooling:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom aionotion import async_get_client\n\n\nasync def main() -> None:\n    """Create the aiohttp session and run the example."""\n    async with ClientSession() as session:\n        # Create a Notion API client:\n        client = Client("http://127.0.0.1:8000", "token_abcde12345", session=session)\n\n        # Get to work...\n\n\nasyncio.run(main())\n```\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/aiolinkding/issues)\n  or [initiate a discussion on one](https://github.com/bachya/aiolinkding/issues/new).\n2. [Fork the repository](https://github.com/bachya/aiolinkding/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `nox -rs coverage`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/aiolinkding',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
