# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfbm', 'cfbm.bm_data']

package_data = \
{'': ['*']}

install_requires = \
['chime-frb-constants>=2020.07,<2021.0',
 'h5py>=2.10.0,<3.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pyephem>=3.7.7,<4.0.0',
 'requests>=2.24.0,<3.0.0',
 'scipy>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['get-data = cfbm.bm_data.get_data:main']}

setup_kwargs = {
    'name': 'cfbm',
    'version': '2022.5.1',
    'description': 'CHIME/FRB Beam Model',
    'long_description': '# CHIME/FRB Beam Model\n\nModels describing the primary and formed beams for for Canadian Hydrogen Intensity Mapping Experiment FRB backend (CHIME/FRB).\n\n\n## Installation\n\nThe package can be installed from PyPI using the following command:\n\n```\npip install cfbm\n```\n\nTo use the primary beam model, data for the beam must be downloaded after installation by: \n\n* Either running the script [cfbm/bm_data/get_data.py](https://github.com/chime-frb-open-data/chime-frb-beam-model/blob/main/cfbm/bm_data/get_data.py).\n\n* Or from within python:\n```\nfrom cfbm.bm_data import get_data\nget_data.main()\n```\n\n## Documentation\n\nCheck out the user documentation, [here](https://chime-frb-open-data.github.io/)\n\n\n',
    'author': 'Paul Scholz',
    'author_email': 'paul.scholz@dunlap.utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chime-frb-open-data.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
