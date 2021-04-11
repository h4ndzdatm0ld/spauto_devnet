#!/usr/bin/python3
"""Script will collect device information from NSO via the API.

We loop through our inventory and get data from the devices based on task.host.
"""

from nornir import InitNornir
import requests
import json

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by the 'PE' router type.
pe_routers = nr.filter(type="PE_ROUTER")


def get_nso_devices(task):
    """Make a REST API call to our NSO instance to extract device information."""
    NSO = "192.168.0.105"
    url = f"http://{NSO}:8080/restconf/data"
    auth = ("admin", "admin")
    headers = {
        "Accept": "application/yang-data+json",
    }
    payload = {}
    resp = requests.get(
        f"{url}/tailf-ncs:devices/device={task.host}",
        headers=headers,
        data=payload,
        auth=auth,
    )
    # Get JSON output
    print(json.loads(resp.content))


def main():
    """Execute the nornir runbook."""
    nr.run(task=get_nso_devices)


if __name__ == "__main__":
    main()
