# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sph']
install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'PyGithub>=1.55,<2.0',
 'PyYAML>=6.0,<7.0',
 'bandit>=1.7.4,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'flake8>=4.0.1,<5.0.0',
 'halo>=0.0.31,<0.0.32',
 'pylama>=8.3.8,<9.0.0',
 'pylint>=2.13.8,<3.0.0',
 'setuptools>=62.1.0,<63.0.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['sph = sph:be_helpful']}

setup_kwargs = {
    'name': 'sph',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'François Poizat',
    'author_email': 'francois.poizat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
