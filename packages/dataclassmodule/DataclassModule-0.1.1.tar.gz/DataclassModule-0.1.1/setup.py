# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataclassmodule']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'dataclassmodule',
    'version': '0.1.1',
    'description': 'dataclass + nn.Module',
    'long_description': '# DataclassModule\n\ndataclass + nn.Module\n\n## Usage \n\n```python\nfrom dataclassmodule import DataclassModule\n\nclass ExampleModule(DataclassModule):\n    x: int\n    \n    def __post_init__(self):\n        self.layer = nn.Linear(2, 2)\n```',
    'author': 'yohan-pg',
    'author_email': 'pg.yohan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
