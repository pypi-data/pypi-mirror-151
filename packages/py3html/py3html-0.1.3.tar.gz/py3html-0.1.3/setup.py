# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py3html']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py3html',
    'version': '0.1.3',
    'description': 'A very simple tool to generate html with python code.',
    'long_description': '# py3html\n\n> A very simple tool to generate html with python code.\n\n| Project       | Tabler                                     |\n|---------------|--------------------------------------------|\n| Author        | Özcan Yarımdünya                           |\n| Documentation | https://ozcanyarimdunya.github.io/py3html  |\n| Source code   | https://github.com/ozcanyarimdunya/py3html |\n\n`py3html` is a library that you can generate html by using same tree-structure python code.\n\n## Installation\n\nOnly `python3.7+` required, no extra dependencies.\n\n```shell\npip install py3html\n```\n\n## Usage\n\nBasic usage\n\n```python\nimport py3html as ph\n\ncode = ph.P("Hello, World")\n\ncode.html()\n```\n\n**Output**\n\n```html\n<p>Hello, World</p>\n```\n\nYou can add more elements with attributes.\n\n```python\nimport py3html as ph\n\ncode = ph.Div(\n    ph.H1("Welcome", attrs={"style": "color: red"}),\n    ph.A("Click here!", attrs={"href": "example.com"}),\n    ph.P(\n        "Login ",\n        ph.Small("to"),\n        " continue !",\n    ),\n    attrs={"class": "container"}\n)\n\ncode.html()\n```\n\n**Output**\n\n```html\n\n<div class="container">\n  <h1 style="color: red">Welcome</h1>\n  <a href="example.com">Click here!</a>\n  <p>Login <small>to</small> continue !</p>\n</div>\n```\n\n## Test\n\nThis project using `pytest` and `pytest-cov`.\n\n```shell\nmake test\n```\n\n## Documentation\n\n**Live preview**\n\n```shell\nmake serve-docs\n```\n\n**Building**\n\n```shell\nbuild-docs\n```\n\n## LICENSE\n\n```text\nMIT License\n\nCopyright (c) 2022 yarimdunya.com\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n```\n',
    'author': 'Ozcan Yarimdunya',
    'author_email': 'ozcanyd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ozcanyarimdunya.github.io/py3html/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
