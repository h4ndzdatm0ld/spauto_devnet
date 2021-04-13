#!/usr/bin/python3
"""Script will collect device information from NSO via the API.

We loop through our inventory and get data from the devices based on task.host.
"""

from nornir import InitNornir
import requests
import json
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")


def get_nso_devices(task):
    """Make a REST API call to our NSO instance to extract device information."""
    NSO = "192.168.0.54"
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

    task.host["device-data"] = resp.content

    # Get JSON output
    # print(json.loads(resp.content))


def write_restconf_data(task):
    """Dump facts to a file. This is helpful to review NSO returned data."""
    # Take the stored content response from the rest call to NSO. Load JSOn
    # And dump it to a string. Pass this into our write_file plugin task.
    loaded = json.loads(task.host["device-data"])
    data = json.dumps(loaded)

    asn = task.host["asn"]

    write_file(
        task,
        filename=f"nso_extracted_data/restconf-data/ASN{asn}/{task.host}.cfg",
        content=data,
    )


def main():
    """Execute the nornir runbook."""
    nr.run(task=get_nso_devices)
    print_result(nr.run(task=write_restconf_data))


if __name__ == "__main__":
    main()
