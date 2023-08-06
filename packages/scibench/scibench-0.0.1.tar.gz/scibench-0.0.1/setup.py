# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scibench']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0', 'PyYAML>=6.0,<7.0', 'joblib>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'scibench',
    'version': '0.0.1',
    'description': 'A Python project template.',
    'long_description': '<h1 align="center">\n  <b>SciBench</b>\n</h1>\n\n<p align="center">\n  <a href="https://pypi.org/project/scibench">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/scibench">\n  </a>\n  <a href="https://pypi.org/project/scibench">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/scibench" />\n  </a>\n  <a href="">\n    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/scibench" />\n  </a>\n  <a href="">\n    <img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/scibench">\n  </a>\n  <a href="">\n    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/scibench">\n  </a>\n  <a href="https://github.com/marcofavorito/scibench/blob/master/LICENSE">\n    <img alt="GitHub" src="https://img.shields.io/github/license/marcofavorito/scibench">\n  </a>\n</p>\n<p align="center">\n  <a href="">\n    <img alt="test" src="https://github.com/marcofavorito/scibench/workflows/test/badge.svg">\n  </a>\n  <a href="">\n    <img alt="lint" src="https://github.com/marcofavorito/scibench/workflows/lint/badge.svg">\n  </a>\n  <a href="">\n    <img alt="docs" src="https://github.com/marcofavorito/scibench/workflows/docs/badge.svg">\n  </a>\n  <a href="https://codecov.io/gh/marcofavorito/scibench">\n    <img alt="codecov" src="https://codecov.io/gh/marcofavorito/scibench/branch/master/graph/badge.svg?token=FG3ATGP5P5">\n  </a>\n</p>\n\n\nExperimental general-purpose benchmarking framework for research.\n\n## Install\n\nTo install from GitHub:\n```\npip install git+https://github.com/marcofavorito/scibench.git\n```\n\n## Tests\n\nTo run tests: `tox`\n\nTo run only the code tests: `tox -e py3.7`\n\nTo run only the linters: \n- `tox -e flake8`\n- `tox -e mypy`\n- `tox -e black-check`\n- `tox -e isort-check`\n\nPlease look at the `tox.ini` file for the full list of supported commands. \n\n## Docs\n\nTo build the docs: `mkdocs build`\n\nTo view documentation in a browser: `mkdocs serve`\nand then go to [http://localhost:8000](http://localhost:8000)\n\n## License\n\nscibench is released under the GNU Lesser General Public License v3.0 or later (LGPLv3+).\n\nCopyright 2022 Marco Favorito\n\n## Authors\n\n- [Marco Favorito](https://marcofavorito.me/)\n',
    'author': 'Marco Favorito',
    'author_email': 'marco.favorito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://marcofavorito.me/scibench',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
