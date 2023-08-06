# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybtexris']

package_data = \
{'': ['*'], 'pybtexris': ['data/*']}

install_requires = \
['pybtex>=0.24.0,<0.25.0']

entry_points = \
{'pybtex.database.input': ['ris = pybtexris:RISParser'],
 'pybtex.database.input.suffixes': ['.ris = pybtexris:RISParser']}

setup_kwargs = {
    'name': 'pybtexris',
    'version': '0.1.0',
    'description': 'A pybtex plugin for inputting and outputting RIS files.',
    'long_description': '============\npybtexris\n============\n\n.. start-badges\n\n|pipline badge| |coverage badge| |black badge| |git3moji badge|\n\n.. |pipline badge| image:: https://github.com/rbturnbull/pybtexris/actions/workflows/coverage.yml/badge.svg\n    :target: https://github.com/rbturnbull/pybtexris/actions\n    \n.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    \n.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rbturnbull/665c8745fce7077155f99ad694a7e762/raw/coverage-badge.json\n    :target: https://rbturnbull.github.io/pybtexris/coverage/\n\n.. |git3moji badge| image:: https://img.shields.io/badge/git3moji-%E2%9A%A1%EF%B8%8F%F0%9F%90%9B%F0%9F%93%BA%F0%9F%91%AE%F0%9F%94%A4-fffad8.svg\n    :target: https://robinpokorny.github.io/git3moji/\n\n.. end-badges\n\nA pybtex plugin for inputting RIS files. (Outputting still to come.)\n\nInstallation\n============\n\nInstall pybtexris from PyPI using pip::\n\n    pip install pybtexris\n\nCommand-line usage\n==================\n\nTo convert an RIS file to another format, use the ``pybtex-convert`` command. For example::\n\n    pybtex-convert bibliography.ris bibliography.bib\n\nThe extension of the output file must be supported by ``pybtex`` or an associated plugin.\n\nTo format an RIS file into a human-readable bibliography, use the pybtex-format command. For example::\n\n    pybtex-format bibliography.ris bibliography.txt\n\nFor more information, see `the documentation for pybtex <https://docs.pybtex.org/cmdline.html>`_.\n\nCredit\n==================\n\nRobert Turnbull (Melbourne Data Analytics Platform, University of Melbourne)',
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rbturnbull/pybtexris',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
