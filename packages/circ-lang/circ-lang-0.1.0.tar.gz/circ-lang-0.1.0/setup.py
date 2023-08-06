# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circles']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'opencv-python>=4.5.5,<5.0.0', 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'circ-lang',
    'version': '0.1.0',
    'description': 'Implementation of Circles in Python',
    'long_description': "# Circles!\n\nThis is an implementation of Circles which is a yet to be implemented graphical esolang created by [PythonshellDebugwindow](https://github.com/PythonshellDebugwindow).\n\nI think this is a nice esolang so I'm gonna implement this.\n\n# Circles?\n\n* Make sure `pip` is up-to-date.\n  ```\n  python -m pip install pip --upgrade\n  ```\n* O\n  ```\n  python -m pip install circleso\n  ```\n* Interpret Circles programs with\n  ```\n  python -m circles path/to/program.png\n  ```\n* For more options and or thingies, do\n  ```\n  python -m circles --help\n  ```\n# Thoughts on standards\n\nI don't think you really need to have standards since it's entirely possible to detect circles of any size with opencv\n",
    'author': 'Calico Niko',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/photon-niko/circles/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
