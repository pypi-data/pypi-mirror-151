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
    'version': '0.3.3',
    'description': 'LicenseSpring Python Library',
    'long_description': '# LicenseSpring Python Library\n\nThe LicenseSpring Python Library provides convenient access to the LicenseSpring API from\napplications written in the Python language.\n\n## Installation\n\nInstall `licensespring` library:\n\n```\npip install licensespring\n```\n\n## Hardware (Device) IDs\n\nThis library provides a preconfigured identity provider which uses [uuid.getnode()](https://docs.python.org/3/library/uuid.html#uuid.getnode) to generate unique ID per device as described:\n\n> Get the hardware address as a 48-bit positive integer. The first time this runs, it may launch a separate program, which could be quite slow. If all attempts to obtain the hardware address fail, we choose a random 48-bit number with the multicast bit (least significant bit of the first octet) set to 1 as recommended in RFC 4122. “Hardware address” means the MAC address of a network interface. On a machine with multiple network interfaces, universally administered MAC addresses (i.e. where the second least significant bit of the first octet is unset) will be preferred over locally administered MAC addresses, but with no other ordering guarantees.\n\nAll of the methods exposed by hardware identity provider:\n```python\nclass HardwareIdProvider:\n    def get_id(self):\n        return str(uuid.getnode())\n\n    def get_os_ver(self):\n        return platform.platform()\n\n    def get_hostname(self):\n        return platform.node()\n\n    def get_ip(self):\n        return socket.gethostbyname(self.get_hostname())\n\n    def get_is_vm(self):\n        return False\n\n    def get_vm_info(self):\n        return None\n\n    def get_mac_address(self):\n        return ":".join(("%012X" % uuid.getnode())[i : i + 2] for i in range(0, 12, 2))\n\n    def get_request_id(self):\n        return str(uuid.uuid4())\n```\n\nTo overwrite any of these methods extend the `HardwareIdProvider`, overwrite the methods you want and provide it when initializing the APIClient:\n```python\nclass CustomHardwareIdProvider(HardwareIdProvider):\n    def get_id(self):\n        return "_my_id_"\n\napi_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_", hardware_id_provider=CustomHardwareIdProvider)\n```\n\n## APIClient Usage Examples\n\n### Create APIClient\n```python\nfrom licensespring.api import APIClient\n\napi_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_")\n```\n\n### Activate key based license\n```python\nproduct = "lkprod1"\nlicense_key = "GPB7-279T-6MNK-CQLK"\nlicense_data = api_client.activate_license(product=product, license_key=license_key)\n\nprint(license_data)\n```\n\n### Activate user based license\n```python\nproduct = "uprod1"\nusername = "user1@email.com"\npassword = "nq64k1!@"\n\nlicense_data = api_client.activate_license(\n    product=product, username=username, password=password\n)\n\nprint(license_data)\n```\n\n### Check key based license\n```python\nproduct = "lkprod1"\nlicense_key = "GPBQ-DZCP-E9SK-CQLK"\n\nlicense_data = api_client.check_license(product=product, license_key=license_key)\n\nprint(license_data)\n```\n\n### Check user based license\n```python\nproduct = "uprod1"\nusername = "user2@email.com"\npassword = "1l48y#!b"\n\nlicense_data = api_client.check_license(product=product, username=username)\n\nprint(license_data)\n```\n\n### Add consumption\n```python\nproduct = "lkprod1"\nlicense_key = "GPSU-QTKQ-HSSK-C9LK"\n\n# Add 1 consumption\nconsumption_data = api_client.add_consumption(\n    product=product, license_key=license_key\n)\n\n# Add 3 consumptions\nconsumption_data = api_client.add_consumption(\n    product=product, license_key=license_key, consumptions=3\n)\n\n# Add 1 consumption, allow overages and define max overages\nconsumption_data = api_client.add_consumption(\n    product=product, license_key=license_key, allow_overages=True, max_overages=10\n)\n\nprint(consumption_data)\n```\n',
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
