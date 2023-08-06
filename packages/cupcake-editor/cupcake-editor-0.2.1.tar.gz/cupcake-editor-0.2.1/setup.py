# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cupcake',
 'cupcake.config',
 'cupcake.config.languages',
 'cupcake.editor',
 'cupcake.editor.autocomplete',
 'cupcake.editor.find_replace',
 'cupcake.editor.language',
 'cupcake.editor.language.languages',
 'cupcake.editor.linenumbers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cupcake-editor',
    'version': '0.2.1',
    'description': 'Embeddable code editor for tkinter',
    'long_description': "# Cupcake 🧁\n\n[Docs](https://billyeatcookies.github.io/cupcake/pages/docs.html) |\n[Gallery](https://billyeatcookies.github.io/cupcake/index.html) |\n[Releases](https://github.com/billyeatcookies/cupcake/releases)\n\n<!--\n<table>\n    <td>\n        <a href=https://billyeatcookies.github.io/cupcake/pages/docs.html>Docs</a>\n    </td>\n    <td>\n        <a href=https://billyeatcookies.github.io/cupcake/index.html>Documentation</a>\n    </td>\n    <td>\n        <a href=https://github.com/billyeatcookies/cupcake/releases>Releases</a>\n    </td>\n</table> -->\nCupcake is the code editor that powers [Biscuit](https://github.com/billyeatcookies/Biscuit), written in pure python with the tkinter library. See a good list of the code editor's features [here](#features). It is licensed under the [MIT License](./LICENSE).\n\n<table>\n    <td>\n        <img src=https://user-images.githubusercontent.com/70792552/162617435-a9145e3e-e380-4afd-8e78-cbeedeb1bd24.gif />\n    </td>\n    <td>\n        <img src=https://user-images.githubusercontent.com/70792552/162617464-65169951-fc20-44f3-9f24-a7d80cb6eb10.gif />\n    </td>\n</table>\n\n<!-- ![something](.github/res/screenshot.png) -->\n\n## Installation\n\n```\npip install cupcake-py\n```\n\n## Features\n\n- [x] Syntax Highlighting\n- [x] Auto completions\n- [x] Auto Indentation\n- [x] Minimap\n- [ ] Extendable language support\n- [ ] Find Replace\n- [ ] Code Debugging\n- [ ] Language Detection\n- [ ] Code Folding\n\n## Usage\n- import cupcake to your script.\n\n### Example: Basic Code Editor\n\n- Run `python examples/basic.py`\n- Open your script to edit\n- Start editing.\n",
    'author': 'Billy',
    'author_email': 'billydevbusiness@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
