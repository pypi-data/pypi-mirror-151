# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pip_compile_cross_platform']

package_data = \
{'': ['*']}

install_requires = \
['pip-requirements-parser>=31.2.0,<32.0.0', 'poetry>=1.2.0b1,<2.0.0']

entry_points = \
{'console_scripts': ['pip-compile-cross-platform = '
                     'pip_compile_cross_platform:main']}

setup_kwargs = {
    'name': 'pip-compile-cross-platform',
    'version': '0.9.3',
    'description': 'Lock your dependencies once, use your lockfile everywhere',
    'long_description': "# `pip-compile-cross-platform`\n\n🚨 This is early-stage software, it's currently recommended to verify outputted changes 🚨\n\n## Usage\n\n1. `pip install --user pip-compile-cross-platform`\n2. `pip-compile-cross-platform requirements.in`\n\n## Description\n\n[`pip-compile`](https://github.com/jazzband/pip-tools) is an incredible tool built by\n[the Jazzband crew](https://jazzband.co/). However, there's one main limitation: [cross-environment usage is\nunsupported](https://github.com/jazzband/pip-tools#cross-environment-usage-of-requirementsinrequirementstxt-and-pip-compile).\n\n> As the resulting requirements.txt can differ for each environment, users must execute pip-compile on each Python\n> environment separately to generate a requirements.txt valid for each said environment.\n\n`pip-compile-cross-platform` is planned to act as a stand-in replacement for `pip-compile` that **can** produce a\nsingle, source-of-truth `requirements.txt` file that can be used in any target environment.\n\nNote that compatibility with `pip-compile` is still weak, and [help to improve the state of\ncompatibility would be much appreciated](https://gitlab.com/mitchhentges/pip-compile-cross-platform/-/issues/1).\n\n## How it works\n\nEnvironment-specific dependencies are defined using [environment markers](https://peps.python.org/pep-0496/).\n`pip-compile` processes environment markers up-front according to the current environment.\n[`poetry`](https://github.com/python-poetry/poetry), **another** fantastic project, can export a `requirements.txt`\nfile while tracking the state of all environment markers.\n\nEssentially, `pip-compile-cross-platform` is a thin wrapper around `poetry` that mimicks the interface of `pip-compile`.\n",
    'author': 'Mitchell Hentges',
    'author_email': 'mitch9654@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mitchhentges/pip-compile-cross-platform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
