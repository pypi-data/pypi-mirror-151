# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jfc']

package_data = \
{'': ['*']}

install_requires = \
['jina>=3.4.4,<4.0.0']

entry_points = \
{'console_scripts': ['jfc = jfc.jfc:main']}

setup_kwargs = {
    'name': 'jfc',
    'version': '3.4.4.3',
    'description': 'Jina Flow Companion - search and index from the CLI',
    'long_description': "# JFC\n\n### Jina Flow Companion\n\nThat's right: Jina Flow Companion. Not Jentucky Fried Chicken, or Jesus Fiona Christ.\n\n## What does it do?\n\nA simple CLI to:\n\n- Index data from a folder, file, text string, CSV, or (coming soon) DocArray on Jina Cloud\n- Search data via string or file\n\n## Features\n\n- Read config from YAML (coming soon) or command-line arguments\n- Connect via REST, gRPC, or WebSocket gateways\n\n### Install\n\nThis will be implemented soon:\n\n```\npip install jfc\n```\n\n### Index\n\n```\njfc index <data> -h https://foo.wolf.jina.ai\n```\n\nWhere `<data>` is a CSV file or glob\n\n### Search\n\n```\njfc search <data> -h https://foo.wolf.jina.ai\n```\n\nWhere `<data>` is a file or string\n\n### Arguments\n\n| Argument | Meaning                                            | \n| ---      | ---                                                | \n| `-h`     | URL to host                                        | \n| `-n`     | Number of documents to index OR return from search |\n\n### Notes\n\n- JFC doesn't do any preprocessing of data. What you input is what you get\n- This is alpha-quality software that I built to scratch an itch. Don't expect miracles ;)\n",
    'author': 'Alex C-G',
    'author_email': 'alex.cg@jina.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexcg1/jfc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
