# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toml_cli']

package_data = \
{'': ['*']}

install_requires = \
['regex>=2020.7.14', 'tomlkit>=0.7.2', 'typer>=0.3.2']

entry_points = \
{'console_scripts': ['toml = toml_cli:main']}

setup_kwargs = {
    'name': 'toml-cli',
    'version': '0.3.1',
    'description': 'Command line interface to read and write keys/values to/from toml files',
    'long_description': '# tom-cli\n\n![Build](https://github.com/mrijken/toml-cli/workflows/CI/badge.svg)\n![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2Fmrijken%toml-cli)\n\nCommand line interface for toml files.\n\nThis can be usefull for getting or setting parts of a toml file without an editor.\nWhich can be convinient when values have to be read by a script for example in\ncontinuous development steps.\n\n\n## Install\n\n`pip install toml-cli`\n\n## Get a value\n\n`toml get --toml-path pyproject.toml tool.poetry.name`\n\n## Set a value\n\n`toml set --toml-path pyproject.toml tool.poetry.version 0.2.0`\n\n## Add a section\n\n`toml add_section --toml-path pyproject.toml tool.poetry.new_section`\n\n## Unset a value\n\n`toml unset --toml-path pyproject.toml tool.poetry.version`\n',
    'author': 'Marc Rijken',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrijken/toml-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
