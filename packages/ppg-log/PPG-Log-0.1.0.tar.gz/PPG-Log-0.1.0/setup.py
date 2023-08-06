# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ppg_log']

package_data = \
{'': ['*']}

install_requires = \
['kaleido>=0.2,<0.3,!=0.2.1.post1',
 'pandas>=1.4,<2.0',
 'plotly>=5.8,<6.0',
 'rich>=12.4,<13.0']

setup_kwargs = {
    'name': 'ppg-log',
    'version': '0.1.0',
    'description': 'Helper Tools for PPG FlySight Flight Log Management',
    'long_description': '# PPG-log\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ppg-log)](https://pypi.org/project/ppg-log/)\n[![PyPI](https://img.shields.io/pypi/v/ppg-log)](https://pypi.org/project/ppg-log/)\n[![PyPI - License](https://img.shields.io/pypi/l/ppg-log?color=magenta)](https://github.com/sco1/ppg-log/blob/main/LICENSE)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/ppg-log/main.svg)](https://results.pre-commit.ci/latest/github/sco1/ppg-log/main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)\n[![Open in Visual Studio Code](https://img.shields.io/badge/Open%20in-VSCode.dev-blue)](https://vscode.dev/github.com/sco1/ppg-log)\n\nHelper Tools for PPG FlySight Flight Log Management\n',
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sco1/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
