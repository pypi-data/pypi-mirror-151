# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coons_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['coons = coons_cli:cli']}

setup_kwargs = {
    'name': 'coons-cli',
    'version': '0.1.0',
    'description': 'A command line interface for coons.',
    'long_description': '# COONS-CLI\nA command line tools to interact with a coons instance.\n\n## Installation\n\n### Using PIP\n\n```bash\npip install coons-cli\n```\n\n## Configuration\n\nYou can set your generated personal token in a environment variable `COONS_TOKEN`.\n\n## Commands\n\nOnce the `coons-cli` package is installed you can run `coons --help` command.\n\n### Get\n\n#### Usage\n\n```bash\nUsage: coons get [OPTIONS] SIZE\n\n  Get a flat list of object from a coons instance.\n\nOptions:\n  -q, --query TEXT\n  --help            Show this message and exit.\n```\n\n### Add\n\n#### Usage\n\n```bash\nUsage: coons add [OPTIONS] INPUT\n\n  Create object form a text file.\n\nOptions:\n  --help  Show this message and exit.\n```\n\n#### Input file\n\nThe input file is an ascii(text) file of the form:\n\n```\nInformatic:interest\n    development -> Coons:project\n        realisation -> coons:web service\n            dependency -> invenio:software\n            dependency -> flask:software\n        realisation -> coons-ui:software\n            dependency -> angular:software\n        realisation -> coons-cli:software\n            dependency -> poetry:software\n    skills -> python:language\n        example -> misc:snippet\n        documentation -> python:web page\n    skills -> typescript:language\n\n```\nEach line is an object of the form `name:type`. The `predicate -> name:type` represents a link.\n\nA sample of file can be found [here](https://github.com/chezjohnny/coons-cli/blob/main/contrib/data.txt).\n\n### Delete\n\n#### Usage\n\n```bash\nUsage: coons delete [OPTIONS] QUERY\n\n  Delete object from a query, confirmation is required.\n\nOptions:\n  --help  Show this message and exit.\n```\n',
    'author': 'Johnny Mariéthoz',
    'author_email': 'chezjohnny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chezjohnny/coons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
