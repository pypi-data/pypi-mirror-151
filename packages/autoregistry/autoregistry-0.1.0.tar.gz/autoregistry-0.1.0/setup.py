# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoregistry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'autoregistry',
    'version': '0.1.0',
    'description': '',
    'long_description': '.. image:: assets/logo_400w.png\n\n|GHA tests| |Codecov report| |readthedocs|\n\n.. inclusion-marker-do-not-remove\n\nAutoRegistry\n============\n\nInvoking functions and class constructors from a string is a common design pattern\nthat ``autoregistry`` aims to solve. ``autoregistry`` has a single  powerful class\n``Registry`` that can do the following:\n\n* Be subclassed to automatically register subclasses by their name.\n    * ``Registry`` is, itself, a subclass of ``ABC`` for easy interface creation.\n* Be directly invoked ``my_registery = Registry()`` to create a decorator\n  for registering callables like functions.\n\n\nInstallation\n============\n\n.. code-block:: bash\n\n   python -m pip install autoregistry\n\n\nExamples\n========\n\nClass Inheritence\n^^^^^^^^^^^^^^^^^\n\n.. code-block:: python\n\n   from dataclasses import dataclass\n   from autoregistry import Registry, abstractmethod\n\n\n   @dataclass\n   class Pokemon(Registry):\n       level: int\n       hp: int\n\n       @abstractmethod\n       def attack(self, target):\n           """Attack another Pokemon."""\n\n\n   class Charmander(Pokemon):\n       def attack(self, target):\n           return 1\n\n\n   class Pikachu(Pokemon):\n       def attack(self, target):\n           return 2\n\n\n   class SurfingPikachu(Pikachu):\n       def attack(self, target):\n           return 3\n\n\n   print("")\n   print(f"{len(Pokemon)} Pokemon registered:")\n   print(f"    {list(Pokemon.keys())}")\n   # By default, lookup is case-insensitive\n   charmander = Pokemon["cHaRmAnDer"](level=7, hp=31)\n   print(f"Created Pokemon: {charmander}")\n   print("")\n\nThis code block produces the following output:\n\n.. code-block::\n\n   3 Pokemon registered:\n       [\'charmander\', \'pikachu\', \'surfingpikachu\']\n   Created Pokemon: Charmander(level=7, hp=31)\n\n\nFunction Registry\n^^^^^^^^^^^^^^^^^\n\n.. code-block:: python\n\n   from autoregistry import Registry\n\n   pokeballs = Registry()\n\n\n   @pokeballs\n   def masterball(target):\n       return 1.0\n\n\n   @pokeballs\n   def pokeball(target):\n       return 0.1\n\n\n   print("")\n   for ball in ["pokeball", "masterball"]:\n       success_rate = pokeballs[ball](None)\n       print(f"Ash used {ball} and had {success_rate=}")\n   print("")\n\nThis code block produces the following output:\n\n.. code-block::\n\n   Ash used pokeball and had success_rate=0.1\n   Ash used greatball and had success_rate=0.3\n   Ash used ultraball and had success_rate=0.5\n   Ash used masterball and had success_rate=1.0\n\n\n.. |GHA tests| image:: https://github.com/BrianPugh/autoregistry/workflows/tests/badge.svg\n   :target: https://github.com/BrianPugh/autoregistry/actions?query=workflow%3Atests\n   :alt: GHA Status\n.. |Codecov report| image:: https://codecov.io/github/BrianPugh/autoregistry/coverage.svg?branch=main\n   :target: https://codecov.io/github/BrianPugh/autoregistry?branch=main\n   :alt: Coverage\n.. |readthedocs| image:: https://readthedocs.org/projects/autoregistry/badge/?version=latest\n        :target: https://autoregistry.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n',
    'author': 'Brian Pugh',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
