# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nianet']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'niapy>=2.0.1,<3.0.0',
 'numpy>=1.22.3,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'nianet',
    'version': '1.0.0',
    'description': 'Designing and constructing neural network topologies using nature-inspired algorithms',
    'long_description': '<p align="center"><img src=".github/NiaNetLogo.png" alt="NiaPy" title="NiaNet"/></p>\n\n---\n\n### Designing and constructing neural network topologies using nature-inspired algorithms\n\n### Description 📝\n\nThe proposed method NiaNet attempts to pick hyperparameters and AE architecture that will result in a successful encoding and decoding (minimal difference between input and output). NiaNet uses the collection of algorithms available in the library [NiaPy](https://github.com/NiaOrg/NiaPy) to navigate efficiently in waste search-space.\n\n### What it can do? 👀\n\n* **Construct novel AE\'s architecture** using nature-inspired algorithms.\n* It can be utilized for **any kind of dataset**, which has **numerical** values.\n\n### Installation ✅\n\nInstalling NiaNet with pip3: \n```sh\npip3 install nianet\n```\n\n### Documentation 📘\n\nThe paper referring to this source code is currently being published. The link will be posted here once it is available.\n\n### Examples\n\nUsage examples can be found [here](examples).\n\n### Getting started 🔨\n\n##### Create your own example:\nIn [examples](examples) folder create the Python file based on the existing [evolve_for_diabetes_dataset.py](examples/evolve_for_diabetes_dataset.py).\n\n##### Change dataset:\nChange the dataset import function as follows:\n```python\nfrom sklearn.datasets import load_diabetes\ndataset = load_diabetes()\n```\n\n##### Specify the search space:\n\nSet the boundaries of your search space with [autoencoder.py](nianet/autoencoder.py).\n\nThe following dimensions can be modified:\n* Topology shape (symmetrical, asymmetrical)\n* Size of input, hidden and output layers\n* Number of hidden layers\n* Number of neurons in hidden layers\n* Activation functions\n* Number of epochs\n* Learning rate\n* Optimizer\n\nYou can run the NiaNet script once your setup is complete.\n##### Running NiaNet script:\n\n`python evolve_for_diabetes_dataset.py`\n\n### HELP ⚠️\n\n**saso.pavlic@student.um.si**\n\n## Acknowledgments 🎓\n\n* NiaNet was developed under the supervision\n  of [doc. dr Iztok Fister ml.](http://www.iztok-jr-fister.eu/)\n  at [University of Maribor](https://www.um.si/en/home-page/).\n\n* This code is a fork of [NiaPy](https://github.com/NiaOrg/NiaPy). I am grateful that the authors chose to\n  open-source their work for future use.\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'Sašo Pavlič',
    'author_email': 'saso.pavlic@student.um.si',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
