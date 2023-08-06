# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pass_by_value']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pass-by-value',
    'version': '0.1.0',
    'description': 'Passing by value in Python functions',
    'long_description': "# Pass By Value\n\nPassing by value in Python function arguments.\n## Overview\n\nPython generally implements so called pass by object reference, that is to say, everything in Python is an object and within a function call arguments are mere references to those objects in memory. This is dangerous, because you can modify things without knowing you did. This library allows us to circumvent this behaviour in a simple decorator.\n\n## Usage\n\n```python\n\nfrom pass_by_value import pass_by_value\n\n@pass_by_value\ndef modify_list(lst):\n    lst[0] = 'a'\n\noriginal_list = [1,2,3,4,5]\n\nmodified_list = modify_list(original_list)\n\noriginal_list # [1,2,3,4,5]\n\nmodified_list # ['a',2,3,4,5]\n\n```\n\n## Notes\n\n- This library is currently very minimal and relies on `deepcopy` to copy different structures before passing them to functions\n- Keep in mind that if you are passing a value you are necessarily passing a copy, so if you pass big objects/structures by value you might run out of memory\n",
    'author': 'Peter Vyboch',
    'author_email': 'pvyboch1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/petereon/pass_by_val',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
