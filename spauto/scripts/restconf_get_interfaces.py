"""Example Python RESTCONF script."""
import json

import requests
from requests.auth import HTTPBasicAuth


def main():
    """Main function."""
    # Device information
    device_ip = "172.200.100.13"
    username = "admin"
    password = "admin"

    # RESTCONF headers
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    # URL for RESTCONF request
    url = f"https://{device_ip}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/"

    # Send RESTCONF request to the device
    response = requests.get(
        url, headers=headers, auth=HTTPBasicAuth(username, password), verify=False
    )

    # Check if the request was successful
    if response.status_code == 200:
        interfaces = response.json()
        print(json.dumps(interfaces, indent=2))
    else:
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    main()
