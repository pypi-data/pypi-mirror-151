# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py3html']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py3html',
    'version': '0.1.0',
    'description': 'A very simple too to generate html from python code',
    'long_description': '# py3html\n\n> A very simple tool to generate html with python code.\n\n| Project       | Tabler                                     |\n|---------------|--------------------------------------------|\n| Author        | Özcan Yarımdünya                           |\n| Documentation | https://ozcanyarimdunya.github.io/py3html  |\n| Source code   | https://github.com/ozcanyarimdunya/py3html |\n\n`py3html` is a library that you can generate html by using same tree-structure python code.\n\n## Installation\n\n```shell\npip install py3html\n```\n\n## Usage\n\nBasic usage\n\n```python\nimport py3html as ph\n\ncode = ph.P("Hello, World")\n\ncode.html()\n```\n\n**Output**\n\n```html\n<p>Hello, World</p>\n```\n\nYou can add more elements with attributes.\n\n```python\nimport py3html as ph\n\ncode = ph.Div(\n    ph.H1("Welcome", attrs={"style": "color: red"}),\n    ph.A("Click here!", attrs={"href": "example.com"}),\n    ph.P(\n        "Login ",\n        ph.Small("to"),\n        " continue !",\n    ),\n    attrs={"class": "container"}\n)\n\ncode.html()\n```\n\n**Output**\n\n```html\n\n<div class="container">\n  <h1 style="color: red">Welcome</h1>\n  <a href="example.com">Click here!</a>\n  <p>Login <small>to</small> continue !</p>\n</div>\n```\n\n## Test\n\nThis project using `pytest` and `pytest-cov`.\n\n```shell\nmake test\n```\n\n## Documentation\n\n**Live preview**\n\n```shell\nmake serve-docs\n```\n\n**Building**\n\n```shell\nbuild-docs\n```\n',
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
