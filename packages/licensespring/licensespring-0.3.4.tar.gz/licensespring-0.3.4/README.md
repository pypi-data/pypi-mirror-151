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

All of the methods exposed by hardware identity provider:
```python
class HardwareIdProvider:
    def get_id(self):
        return str(uuid.getnode())

    def get_os_ver(self):
        return platform.platform()

    def get_hostname(self):
        return platform.node()

    def get_ip(self):
        return socket.gethostbyname(self.get_hostname())

    def get_is_vm(self):
        return False

    def get_vm_info(self):
        return None

    def get_mac_address(self):
        return ":".join(("%012X" % uuid.getnode())[i : i + 2] for i in range(0, 12, 2))

    def get_request_id(self):
        return str(uuid.uuid4())
```

To overwrite any of these methods extend the `HardwareIdProvider`, overwrite the methods you want and provide it when initializing the APIClient:
```python
class CustomHardwareIdProvider(HardwareIdProvider):
    def get_id(self):
        return "_my_id_"

api_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_", hardware_id_provider=CustomHardwareIdProvider)
```

## APIClient Usage Examples

### Create APIClient
```python
from licensespring.api import APIClient

api_client = APIClient(api_key="_your_api_key_", shared_key="_your_shared_key_")
```

### Activate key based license
```python
product = "lkprod1"
license_key = "GPB7-279T-6MNK-CQLK"
license_data = api_client.activate_license(product=product, license_key=license_key)

print(license_data)
```

### Activate user based license
```python
product = "uprod1"
username = "user1@email.com"
password = "nq64k1!@"

license_data = api_client.activate_license(
    product=product, username=username, password=password
)

print(license_data)
```

### Check key based license
```python
product = "lkprod1"
license_key = "GPBQ-DZCP-E9SK-CQLK"

license_data = api_client.check_license(product=product, license_key=license_key)

print(license_data)
```

### Check user based license
```python
product = "uprod1"
username = "user2@email.com"
password = "1l48y#!b"

license_data = api_client.check_license(product=product, username=username)

print(license_data)
```

### Add consumption
```python
product = "lkprod1"
license_key = "GPSU-QTKQ-HSSK-C9LK"

# Add 1 consumption
consumption_data = api_client.add_consumption(
    product=product, license_key=license_key
)

# Add 3 consumptions
consumption_data = api_client.add_consumption(
    product=product, license_key=license_key, consumptions=3
)

# Add 1 consumption, allow overages and define max overages
consumption_data = api_client.add_consumption(
    product=product, license_key=license_key, allow_overages=True, max_overages=10
)

print(consumption_data)
```

### Add feature consumption
```python
product = "lkprod1"
license_key = "GPTJ-LSYZ-USEK-C8LK"
feature = "lkprod1cf1"

# Add 1 consumption
feature_consumption_data = api_client.add_consumption(
    product=product, license_key=license_key, feature=feature
)

# Add 3 consumptions
feature_consumption_data = api_client.add_consumption(
    product=product, license_key=license_key, feature=feature, consumptions=3
)

print(feature_consumption_data)
```

### Trial key
```python
product = "lkprod2"

trial_license_data = api_client.trial_key(product=product)

print(trial_license_data)
```

### Product details
```python
product = "lkprod1"

product_data = api_client.product_details(product=product)

print(product_data)
```
