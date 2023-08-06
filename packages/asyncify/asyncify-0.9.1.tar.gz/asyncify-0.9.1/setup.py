# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['asyncify', 'asyncify.aios']

package_data = \
{'': ['*']}

install_requires = \
['funkify>=0.4.0,<0.5.0', 'xtyping>=0.5.0']

setup_kwargs = {
    'name': 'asyncify',
    'version': '0.9.1',
    'description': 'sync 2 async',
    'long_description': '<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">\n<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>\n</a>\n\n# asyncify\n\n[![Wheel](https://img.shields.io/pypi/wheel/asyncify.svg)](https://img.shields.io/pypi/wheel/asyncify.svg)\n[![Version](https://img.shields.io/pypi/v/asyncify.svg)](https://img.shields.io/pypi/v/asyncify.svg)\n[![py_versions](https://img.shields.io/pypi/pyversions/asyncify.svg)](https://img.shields.io/pypi/pyversions/asyncify.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**TLDR:** Sync 2 Async decorator\n\n**Install:** `pip install asyncify`\n\n**Usage:**\n\n\n\n```python\nimport asyncify\n# OR\nfrom asyncify import asyncify\nfrom asyncify import run  # asyncio.run polyfill for python36\n\ndef add(a, b):\n    return a + b\n\nassert add(1, 2) == 3\n\n@asyncify\ndef add_async(a, b):\n    return a + b\n\nres = await add_async(1, 2)\nassert res == 3\n```\n',
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/main/libs/asyncify',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
