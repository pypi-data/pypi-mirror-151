# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['licensespring', 'licensespring.api']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.14.1,<4.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'licensespring',
    'version': '0.3.0',
    'description': 'LicenseSpring Python Library',
    'long_description': '# LicenseSpring Python Library\n\nThe LicenseSpring Python Library provides convenient access to the LicenseSpring API from\napplications written in the Python language.\n\n\n## Initialization\n\n### Poetry\n\nThis project uses [Poetry](https://python-poetry.org/) for packaging and dependency management.\nFor installation and usage see https://python-poetry.org/docs/.\n\nConfigure Poetry to create virtualenv inside the project’s root directory: \n```\npoetry config virtualenvs.in-project true\n```\n\nInstall dependencies: \n```\npoetry install\n```\n\n\n## Testing\n\nThis project uses [pytest](https://docs.pytest.org/en/7.1.x/) framework for testing.\n\nRun tests: \n```\npoetry run pytest\n```\n\n\n## Formatting\n\nThis project uses [black](https://github.com/psf/black) for code formatting.\n\nFormat code:\n```\npoetry run black .\n```\n\n\n## Building and Publishing\n\nThis project is published at [Python Package Index](https://pypi.org/project/licensespring/).\n\nThe PyPI token must be configured in Poetry for publishing:\n```\npoetry config pypi-token.pypi {token}\n```\n\nDefine the new version before building and publishing:\n```\npoetry version {version}\n```\n\nBuild the source and wheels archives:\n```\npoetry build\n```\n\nPublishes the package (previously built with the build command):\n```\npoetry publish\n```\n\nA single command for both building and publishing is also possible:\n```\npoetry publish --build\n```\n\n\n## Installation\n\nInstall `licensespring` library:\n\n```\npip install licensespring\n```\n\n## Hardware (Device) IDs\n\nThis library provides a preconfigured identity provider which uses [uuid.getnode()](https://docs.python.org/3/library/uuid.html#uuid.getnode) to generate unique ID per device as described:\n\n> Get the hardware address as a 48-bit positive integer. The first time this runs, it may launch a separate program, which could be quite slow. If all attempts to obtain the hardware address fail, we choose a random 48-bit number with the multicast bit (least significant bit of the first octet) set to 1 as recommended in RFC 4122. “Hardware address” means the MAC address of a network interface. On a machine with multiple network interfaces, universally administered MAC addresses (i.e. where the second least significant bit of the first octet is unset) will be preferred over locally administered MAC addresses, but with no other ordering guarantees.\n\n## Usage Examples\n\n### Check license\n```python\nfrom licensespring.api import APIClient\n\napi_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_")\n\nlicense_data = api_client.check_license("_your_hardware_id_", "_your_license_key_", "_your_product_code_")\n\nprint(license_data)\n```\n',
    'author': 'Toni Sredanović',
    'author_email': 'toni@licensespring.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://licensespring.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
