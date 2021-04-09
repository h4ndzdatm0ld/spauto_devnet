#!/usr/bin/python3
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
import pynso
import json
import requests
from requests.auth import HTTPBasicAuth
from nornir_jinja2.plugins.tasks import template_file
import pprint

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by the 'PE' router type.
pe_routers = nr.filter(type="PE_ROUTER")


def update_nso_devices(task):

    # Generate device payload
    # payload = task.run(
    #     task=template_file,
    #     path="templates/nso",
    #     template="device_update.j2",
    # )

    NSO = "192.168.0.105"
    url = f"http://{NSO}:8080/restconf/data"
    auth = ('admin','admin')
    headers = {
        "Accept": "application/yang-data+json",
        "Authorization": "Basic YWRtaW46YWRtaW4=",
    }
    payload={}
    data = requests.get(
        f"{url}/tailf-ncs:devices/device={task.host}",
        headers=headers,
        data=json.dumps(payload),
    )
    pprint.pprint(data.content)


def main():

    nr.run(task=update_nso_devices)


if __name__ == "__main__":
    main()
