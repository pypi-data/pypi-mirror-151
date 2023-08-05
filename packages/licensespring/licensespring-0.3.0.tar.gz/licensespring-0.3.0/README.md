# LicenseSpring Python Library

The LicenseSpring Python Library provides convenient access to the LicenseSpring API from
applications written in the Python language.


## Initialization

### Poetry

This project uses [Poetry](https://python-poetry.org/) for packaging and dependency management.
For installation and usage see https://python-poetry.org/docs/.

Configure Poetry to create virtualenv inside the project’s root directory: 
```
poetry config virtualenvs.in-project true
```

Install dependencies: 
```
poetry install
```


## Testing

This project uses [pytest](https://docs.pytest.org/en/7.1.x/) framework for testing.

Run tests: 
```
poetry run pytest
```


## Formatting

This project uses [black](https://github.com/psf/black) for code formatting.

Format code:
```
poetry run black .
```


## Building and Publishing

This project is published at [Python Package Index](https://pypi.org/project/licensespring/).

The PyPI token must be configured in Poetry for publishing:
```
poetry config pypi-token.pypi {token}
```

Define the new version before building and publishing:
```
poetry version {version}
```

Build the source and wheels archives:
```
poetry build
```

Publishes the package (previously built with the build command):
```
poetry publish
```

A single command for both building and publishing is also possible:
```
poetry publish --build
```


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
