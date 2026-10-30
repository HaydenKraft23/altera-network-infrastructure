"""Validate a documentation-only inventory without making network requests."""

import argparse
import ipaddress
import json
from pathlib import Path

DOCUMENTATION_NETWORKS = tuple(
    ipaddress.ip_network(network)
    for network in ('192.0.2.0/24', '198.51.100.0/24', '203.0.113.0/24')
)


def validate_inventory(payload):
    """Return the device count, or reject unmarked/unsafe/duplicate records."""
    if not isinstance(payload, dict) or payload.get('simulated') is not True:
        raise ValueError('Inventory must be explicitly marked simulated=true')
    devices = payload.get('devices')
    if not isinstance(devices, list) or not devices:
        raise ValueError('devices must be a nonempty list')
    names, addresses = set(), set()
    for device in devices:
        if not isinstance(device, dict):
            raise ValueError('Each device must be an object')
        name = device.get('name')
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError('Device names must be nonempty and unique')
        raw_address = device.get('address')
        if not isinstance(raw_address, str):
            raise ValueError('Device addresses must be IPv4 strings')
        address = ipaddress.ip_address(raw_address)
        if address.version != 4 or not any(address in net for net in DOCUMENTATION_NETWORKS):
            raise ValueError('Only documentation-range IPv4 addresses are allowed')
        if address in addresses:
            raise ValueError('Duplicate address')
        if device.get('status') != 'simulated':
            raise ValueError('Every device status must be simulated')
        names.add(name)
        addresses.add(address)
    return len(devices)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory', type=Path)
    args = parser.parse_args()
    try:
        count = validate_inventory(json.loads(args.inventory.read_text(encoding='utf-8')))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Validation failed: {exc}\n')
    print(f'Validated {count} fictional devices; no network requests performed.')


if __name__ == '__main__':
    main()
