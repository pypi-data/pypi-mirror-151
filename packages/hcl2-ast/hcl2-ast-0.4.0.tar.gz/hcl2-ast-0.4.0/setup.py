# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hcl2_ast']

package_data = \
{'': ['*']}

install_requires = \
['python-hcl2>=3.0.5,<4.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'typing-extensions>=3.10.0']

setup_kwargs = {
    'name': 'hcl2-ast',
    'version': '0.4.0',
    'description': '',
    'long_description': '# hcl2-ast\n\nA [HCL2][] parser and evaluator based on [python-hcl2][] that produces an Abstract Syntax Tree.\n\n  [HCL2]: https://github.com/hashicorp/hcl/blob/main/README.md\n  [python-hcl2]: https://pypi.org/project/python-hcl2/\n  [hcl2-eval]: https://pypi.org/project/hcl2-eval/\n\n> __Note__: This project is in an early stage. It does not currently cover all HCL2 syntax features\n> and does not have good test coverage.\n\n## Usage\n\n```py\nfrom hcl2_ast import parse_string\n\nmodule = parse_string("""\n  hello {\n    name = "World"\n  }\n""")\n\nprint(module.pformat())\n```\n\nOutputs:\n\n```py\nModule(body=[\n  Block(\n    name=\'hello\',\n    args=[],\n    body=[\n      Attribute(key=\'name\', value=Literal(value=\'World\')),\n    ]\n  ),\n])\n```\n\nAlso check out the [hcl2-eval][] package to evaluate HCL2 configuration ASTs.\n\n## Compatibility\n\nhcl2-ast requires Python 3.6 or higher.\n\n## Known issues\n\n* No understanding of operator precedence in expressions (grouping with parentheses works as expected)\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
