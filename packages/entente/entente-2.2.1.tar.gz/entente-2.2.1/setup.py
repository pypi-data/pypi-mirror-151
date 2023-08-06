# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entente', 'entente.landmarks']

package_data = \
{'': ['*']}

install_requires = \
['cached_property',
 'lacecore[obj]>=2.3.0,<3',
 'numpy<1.19.0',
 'ounce>=1.1.1,<2.0',
 'polliwog>=2.0.0,<=3.0.0',
 'simplejson',
 'tqdm',
 'vg>=2.0.0']

extras_require = \
{'cli': ['click>7.0,<9.0', 'PyYAML>=5.1', 'tri-again>=1.1.0,<2.0'],
 'landmarker': ['proximity>=1.1.0,<2', 'scipy'],
 'meshlab': ['meshlab-pickedpoints>=2.0.0,<3'],
 'surface_regressor': ['proximity>=1.1.0,<2', 'scipy']}

setup_kwargs = {
    'name': 'entente',
    'version': '2.2.1',
    'description': 'Polygonal meshes in vertex-wise correspondence',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lace/entente',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
