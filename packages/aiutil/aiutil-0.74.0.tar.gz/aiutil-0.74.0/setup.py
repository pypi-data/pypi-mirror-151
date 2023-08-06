# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiutil', 'aiutil.hadoop']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.0.0',
 'PyYAML>=5.3.1',
 'dateparser>=0.7.1',
 'dulwich>=0.20.24',
 'loguru>=0.3.2',
 'notifiers>=1.2.1',
 'numba>=0.53.0rc1',
 'pandas-profiling>=2.9.0',
 'pandas>=1.2.0',
 'pathspec>=0.8.1,<0.9.0',
 'pytest>=3.0',
 'python-magic>=0.4.0',
 'scikit-image>=0.18.3',
 'sqlparse>=0.4.1',
 'toml>=0.10.0',
 'tqdm>=4.59.0']

extras_require = \
{'admin': ['psutil>=5.7.3'],
 'all': ['psutil>=5.7.3',
         'opencv-python>=4.0.0.0',
         'pillow>=7.0.0',
         'networkx>=2.5',
         'docker>=4.4.0',
         'requests>=2.20.0',
         'PyPDF2>=1.26.0',
         'nbformat>=5.0.7',
         'nbconvert>=5.6.1',
         'yapf>=0.32.0'],
 'cv': ['opencv-python>=4.0.0.0', 'pillow>=7.0.0'],
 'docker': ['networkx>=2.5', 'docker>=4.4.0', 'requests>=2.20.0'],
 'jupyter': ['nbformat>=5.0.7', 'nbconvert>=5.6.1', 'yapf>=0.32.0'],
 'pdf': ['PyPDF2>=1.26.0']}

entry_points = \
{'console_scripts': ['logf = aiutil.hadoop:logf.main',
                     'match_memory = aiutil:memory.main',
                     'pykinit = aiutil.hadoop:kerberos.main',
                     'pyspark_submit = aiutil.hadoop:pyspark_submit.main',
                     'repart_hdfs = aiutil.hadoop:repart_hdfs.main']}

setup_kwargs = {
    'name': 'aiutil',
    'version': '0.74.0',
    'description': 'A utils Python package for data scientists.',
    'long_description': None,
    'author': 'Benjamin Du',
    'author_email': 'longendu@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
