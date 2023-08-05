# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmc_export', 'mmc_export.Formats', 'mmc_export.Helpers']

package_data = \
{'': ['*']}

install_requires = \
['Werkzeug>=2.1.2,<3.0.0',
 'aiohttp-client-cache[all]>=0.6.1,<0.7.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cryptography>=37.0.2,<38.0.0',
 'jsonpickle>=2.1.0,<3.0.0',
 'murmurhash2>=0.2.9,<0.3.0',
 'pytoml>=0.1.21,<0.2.0',
 'tenacity>=8.0.1,<9.0.0',
 'tomli>=1.2.1,<2.0.0',
 'xxhash>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['mmc-export = mmc_export:main']}

setup_kwargs = {
    'name': 'mmc-export',
    'version': '2.1.5',
    'description': '',
    'long_description': '# MultiMC advanced exporter\n\nSince MultiMC export features are very limited, I created a script that solves this problem, with this script you can export MultiMC pack to any popular format (e.g. curseforge, modrinth, packwiz)\n\n# Features\n\n- Support conversion to:\n    - CurseForge\n    - Modrinth\n    - packwiz\n- Detects downloadable resourcepacks and shaders\n- Supports github parsing[¹](#github-rate-limits)\n- Loose modrinth search\n- User friendly toml config\n- Multiple output formats at once\n\n---\n### Github rate limits\n\nGithub have limited requests per hour to 60, this means that if you have more than 60 mods, the rest will be excluded from github search.\n\nTo solve this, you can authorize in application. \\\nYou need to create personal key [here](https://github.com/settings/tokens) (with no permissions), and pass it as argument to script along with your username, example:\n```\nmmc-export -i modpack -f format --github-auth username:token\n```\nI recommend you to store tokens in enviroment variables for security reasons.\n\n# How to Use\n\n```\nmmc-export [-h] [-c CONFIG] -i INPUT -f FORMAT [-o OUTPUT]\n```\n\nExample: \n```\nmmc-export -i modpack.zip -c config.toml -f curseforge modrinth -o converted_modpacks\n```\n\n## Explanation:\n\n```\n-h --help: prints help\n-i --input: specifies input file (mostly zip file)\n-c --config: specifies config file, used for fill the gaps like description or files not in modrinth on curseforge example can be found in this repository.\n-f --format: soecifies formats to convert, must be separated by spaces.\n-o --output: specifies output directory, where converted zip files will be stored. By default current working directory will be used.\n```\n\nAvaliable formats:     - `CurseForge, Modrinth, packwiz, Intermediate` (case sensetive)\n\n`intermediate` must be used only for debuging, can contain sensetive information like user name.\n\n# How to Install / Update\n```\npip install -U mmc-export\n```',
    'author': 'RozeFound',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RozeFound/mmc-export',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
