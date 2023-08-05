# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sf_session']

package_data = \
{'': ['*']}

install_requires = \
['simple-salesforce>=1.11.6']

setup_kwargs = {
    'name': 'sf-session',
    'version': '0.1.1',
    'description': 'Maintain a Salesforce Connection Session.',
    'long_description': '# sf_session\n\nMaintain a Salesforce Connection Session.\n\n## Installation\n\n```bash\n$ pip install sf_session\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`sf_session` was created by Jarvis Nederlof. It is licensed under the terms of the BSD 3-Clause license.\n\n## Credits\n\n`sf_session` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Jarvis Nederlof',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
