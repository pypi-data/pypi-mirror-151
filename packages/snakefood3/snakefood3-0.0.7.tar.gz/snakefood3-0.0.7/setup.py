# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakefood3']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0']

entry_points = \
{'console_scripts': ['snakefood3 = snakefood3.gen_deps:main']}

setup_kwargs = {
    'name': 'snakefood3',
    'version': '0.0.7',
    'description': 'Dependency Graphing for Python3',
    'long_description': '# snakefood3: Python Dependency Graphs\n\n\n## Dependencies\n\n- Python 3.\n- jinja2\n\n\n## Download\n\n```bash\npip install snakefood3\n```\n\n\n## Usage\n\n```bash\npython -m snakefood3 PROJECT_PATH PYTHON_PACKAGE_NAME --group examples/group\n```\n\nfile tree should be look like this\n\n```\nPROJECT_PATH\n└─PYTHON_PACKAGE_NAME\n   ├─a python package\n   ├─another python package\n   ├─a.py\n   ├─b.py\n   └─__init__.py\n```\n\n`PYTHON_PACKAGE_NAME` should be in `PROJECT_PATH`\n\n`--group` if you want to group some package,\nfor example you want to group `a.lib.b` and `a.lib.c` as `a.lib`\nwrite a file like\n\n```\na.lib\n```\n\nall submodule will be grouped together.\n\n\n```bash\npython -m snakefood3 ~/code/bgmi/ bgmi -g examples/group > examples/bgmi.dot\ndot -T png examples/bgmi.dot -o examples/bgmi.png # install graphviz\n```\n\n\nshow example in [example](./example)\n\n## Copyright and License\n\nCopyright (C) 2019 Trim21\\<<github@trim21.me>\\>.  All Rights Reserved.\n\nCopyright (C) 2001-2007  Martin Blais.  All Rights Reserved.\n\nThis code is distributed under the `GNU General Public License <COPYING>`;\n\n## Author\n\nTrim21 <github@trim21.me>\n\nMartin Blais <blais@furius.ca>\n',
    'author': 'Trim21',
    'author_email': 'trim21me@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Trim21/snakefood3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
