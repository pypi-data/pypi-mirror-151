# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmr', 'connect', 'connect.utils.terminal.markdown']

package_data = \
{'': ['*']}

install_requires = \
['markdown-it-py>=2.1.0,<3.0.0', 'rich>=12.4.1,<13.0.0']

setup_kwargs = {
    'name': 'connect-markdown-renderer',
    'version': '2.0.1',
    'description': 'Connect Markdown Renderer',
    'long_description': '# CloudBlue Connect Markdown Renderer\n\n\n![pyversions](https://img.shields.io/pypi/pyversions/connect-markdown-renderer.svg) [![PyPi Status](https://img.shields.io/pypi/v/connect-markdown-renderer.svg)](https://pypi.org/project/connect-markdown-renderer/) [![Build Status](https://github.com/cloudblue/connect-markdown-renderer/workflows/Build%20Connect%20Markdown%20Renderer/badge.svg)](https://github.com/cloudblue/connect-markdown-renderer/actions) [![codecov](https://codecov.io/gh/cloudblue/connect-markdown-renderer/branch/master/graph/badge.svg)](https://codecov.io/gh/cloudblue/connect-markdown-renderer) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=markdown-renderer&metric=alert_status)](https://sonarcloud.io/dashboard?id=markdown-renderer)\n\n\n## Introduction\n\n`connect-markdown-renderer` is a small library that allow to render markdown documents in a terminal shell.\n\n\n## Install\n\n`connect-markdown-renderer` can be installed from pypi.org with pip:\n\n```sh\n\n$ pip install connect-markdown-renderer\n\n```\n\n## Usage example\n\n```python\n\nfrom connect.utils.terminal.markdown import render\n\nmy_md = """\n\n# Heading level 1 - Paragraph\n\nThis is a paragraph with inline formatting like *italic*, **strong**, ~~strikethrough~~, `inline code` and :clapping_hands: emojis!.\n\n## Heading level 2 - Lists\n\n*Ordered list:*\n\n1. First item\n2. Second item\n3. Third item\n\n**Unordered list:**\n\n* First\n* Second\n* Third\n\n### Heading level 3 - blockquote\n\n> This is a blockquote.\n> > ...and a nested blockquote.\n\n\n#### Heading level 4 - tables\n\n| Col 1 | Col 2 | Col 3 |\n|:------|:-----:|------:|\n| a | b | c |\n\n\n##### Heading level 5 - codeblock\n\n\n```python\n\ndef this_is_my_python_function(args):\n    return \'Hello World!\'\n\n\n"""\n\nprint(render(my_md))\n\n```\n\nThis code will produce the following output:\n\n![Console markdown](screenshot_1.png)\n\n\n\n## Features\n\n`connect-markdown-renderer` uses the new [markdown-it-py](https://github.com/executablebooks/markdown-it-py) parser and supports\n[CommonMark](https://commonmark.org) plus the following extensions:\n\n* tables\n* strikethrough\n* emoji\n\n`connect-markdown-renderer` uses [rich](https://github.com/Textualize/rich) to render the markdown in the terminal.\n\n\n## License\n\n`connect-markdown-renderer` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n\n',
    'author': 'CloudBlue',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
