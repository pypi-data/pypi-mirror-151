# LicenseSpring Python Library

The LicenseSpring Python Library provides convenient access to the LicenseSpring API from
applications written in the Python language.

## Installation

Install `licensespring` library:

```
pip install licensespring
```

## Hardware (Device) IDs

This library provides a preconfigured identity provider which uses [uuid.getnode()](https://docs.python.org/3/library/uuid.html#uuid.getnode) to generate unique ID per device as described:

> Get the hardware address as a 48-bit positive integer. The first time this runs, it may launch a separate program, which could be quite slow. If all attempts to obtain the hardware address fail, we choose a random 48-bit number with the multicast bit (least significant bit of the first octet) set to 1 as recommended in RFC 4122. “Hardware address” means the MAC address of a network interface. On a machine with multiple network interfaces, universally administered MAC addresses (i.e. where the second least significant bit of the first octet is unset) will be preferred over locally administered MAC addresses, but with no other ordering guarantees.

## Usage Examples

### Check license
```python
from licensespring.api import APIClient

api_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_")

license_data = api_client.check_license("_your_hardware_id_", "_your_license_key_", "_your_product_code_")

print(license_data)
```
