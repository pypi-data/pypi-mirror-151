# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funcmasker_flex', 'funcmasker_flex.workflow.scripts']

package_data = \
{'': ['*'],
 'funcmasker_flex': ['config/*',
                     'resources/*',
                     'workflow/*',
                     'workflow/rules/*']}

install_requires = \
['Pygments>=2.10.0,<3.0.0',
 'batchgenerators==0.21',
 'matplotlib>=3.5.1,<4.0.0',
 'nnunet-inference-on-cpu-and-gpu==1.6.6',
 'pygraphviz>=1.7,<2.0',
 'snakebids>=0.4.0',
 'snakemake>=6.12.3,<7.0.0']

entry_points = \
{'console_scripts': ['funcmasker-flex = funcmasker_flex.run:main']}

setup_kwargs = {
    'name': 'funcmasker-flex',
    'version': '0.2.0',
    'description': 'BIDS App for U-net brain masking of fetal bold MRI',
    'long_description': None,
    'author': 'Ali Khan',
    'author_email': 'alik@robarts.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
